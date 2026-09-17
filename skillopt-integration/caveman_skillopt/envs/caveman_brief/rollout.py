"""
Rollout for the caveman_brief SkillOpt environment.

One episode = one compression / drafting task. The **skill document under
training is injected as the system prompt**, which is exactly how the skill
will be used at deployment time (a pasted rule file in front of a frozen
model). No extra inference-time calls are added, so the artifact SkillOpt
produces stays zero-overhead.

The trajectory for each episode is persisted at
``<out_root>/predictions/<id>/conversation.json`` because the shared
``EnvAdapter.reflect()`` reads that exact path; without it the reflection
stage cannot produce learning patches.
"""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from skillopt.model import chat_target

from .evaluator import evaluate

_ROLLOUT_HEADER = (
    "You are being evaluated on token-efficient professional writing. "
    "Follow the skill below exactly."
)

_REGISTER_TASK_NOTE = {
    "be_brief": (
        "Output the rewritten text only. Professional prose with full grammar; "
        "cut every word that is not doing work; keep every fact, number, name, "
        "date and citation. Do not explain what you cut."
    ),
    "caveman": (
        "Answer terse. Fragments are allowed. All technical substance stays, "
        "fluff dies. Code, commands, file paths and exact error strings are "
        "never compressed."
    ),
    "unified": (
        "Reason internally in the grug voice, but output professional prose. "
        "Code, commands, paths and error strings stay byte-for-byte exact."
    ),
    "grug_reasoning": (
        "Put your internal reasoning inside <thinking>...</thinking> using the "
        "SNIFF / FEAR / PLAN / ACT / SPEAK flow, in the grug voice, under the "
        "word budget. Output only the professional answer outside that block. "
        "Never let the grug voice appear in the visible answer."
    ),
}


def _build_system(skill_content: str) -> str:
    skill = (skill_content or "").strip()
    if not skill:
        return _ROLLOUT_HEADER
    return f"{_ROLLOUT_HEADER}\n\n## Skill\n{skill}\n"


def _build_user(item: dict) -> str:
    instruction = str(item.get("instruction") or "").strip()
    source = str(item.get("source") or "").strip()
    register = str(item.get("register") or "be_brief").strip().lower()
    note = _REGISTER_TASK_NOTE.get(register, _REGISTER_TASK_NOTE["be_brief"])

    parts: list[str] = []
    if instruction:
        parts.append(instruction)
    parts.append(note)
    if source:
        parts.append(f"---\n{source}\n---")
    return "\n\n".join(parts)


def _rollout_one(
    item: dict,
    skill_content: str,
    *,
    prediction_dir: Path,
    max_completion_tokens: int,
) -> dict:
    system = _build_system(skill_content)
    user = _build_user(item)

    # A single transient API failure must not abort the whole epoch, but a
    # total outage must not be silently scored as a bad skill either. We
    # degrade per item, and run_batch re-raises when every item failed.
    try:
        prediction, _usage = chat_target(
            system=system,
            user=user,
            max_completion_tokens=max_completion_tokens,
        )
    except Exception as exc:  # noqa: BLE001 - surfaced as a scored error below
        return {
            "id": str(item.get("id") or ""),
            "hard": 0,
            "soft": 0.0,
            "predicted_answer": "",
            "task_description": str(item.get("instruction") or "")[:500],
            "question": user,
            "reference_text": str(item.get("source") or ""),
            "task_type": str(item.get("task_type") or "prose"),
            "register": str(item.get("register") or "be_brief"),
            "language": str(item.get("language") or "en"),
            "target_system_prompt": system,
            "target_user_prompt": user,
            "n_turns": 1,
            "violations": ["target_call_failed"],
            "error": f"{type(exc).__name__}: {exc}",
        }

    score = evaluate(item, prediction)

    # EnvAdapter.reflect() reads this exact trajectory path.
    item_id = str(item.get("id") or "")
    safe_id = "".join(c if c.isalnum() or c in "-_." else "_" for c in item_id) or "item"
    task_dir = prediction_dir / safe_id
    task_dir.mkdir(parents=True, exist_ok=True)
    conversation = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
        {"role": "assistant", "content": prediction},
    ]
    (task_dir / "conversation.json").write_text(
        json.dumps(conversation, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result = score.to_dict()
    result.pop("details", None)
    result.update(
        {
            "id": item_id,
            "hard": score.hard,
            "soft": score.soft,
            "predicted_answer": prediction,
            "task_description": str(item.get("instruction") or "")[:500],
            "question": user,
            "reference_text": str(item.get("source") or ""),
            "task_type": str(item.get("task_type") or "prose"),
            "register": str(item.get("register") or "be_brief"),
            "language": str(item.get("language") or "en"),
            "target_system_prompt": system,
            "target_user_prompt": user,
            "n_turns": 1,
            "violations": score.violations,
            "score_details": score.details,
        }
    )
    return result


def run_batch(
    *,
    items: list[dict],
    skill_content: str,
    out_root: str,
    workers: int = 8,
    max_completion_tokens: int = 4096,
) -> list[dict]:
    """Run a batch of episodes, score them, and persist their trajectories."""
    os.makedirs(out_root, exist_ok=True)
    prediction_dir = Path(out_root) / "predictions"
    prediction_dir.mkdir(parents=True, exist_ok=True)

    if not items:
        return []

    workers = max(1, int(workers))
    if workers == 1 or len(items) == 1:
        results = [
            _rollout_one(
                item,
                skill_content,
                prediction_dir=prediction_dir,
                max_completion_tokens=max_completion_tokens,
            )
            for item in items
        ]
    else:
        results = [None] * len(items)
        with ThreadPoolExecutor(max_workers=min(workers, len(items))) as pool:
            futures = {
                pool.submit(
                    _rollout_one,
                    item,
                    skill_content,
                    prediction_dir=prediction_dir,
                    max_completion_tokens=max_completion_tokens,
                ): index
                for index, item in enumerate(items)
            }
            for future in as_completed(futures):
                index = futures[future]
                results[index] = future.result()

    # If every episode failed the target call, this is an infrastructure
    # outage rather than a weak skill. Fail loudly instead of returning a
    # batch of zeros that the optimizer would try to "fix".
    if all(result.get("error") for result in results):
        first = results[0].get("error", "unknown error")
        raise RuntimeError(
            f"All {len(results)} rollouts failed the target model call — "
            f"check your backend credentials and endpoint. First error: {first}"
        )

    (Path(out_root) / "rollouts.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return results
