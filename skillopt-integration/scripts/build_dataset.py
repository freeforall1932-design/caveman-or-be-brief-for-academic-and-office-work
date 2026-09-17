#!/usr/bin/env python3
"""
Build the caveman_brief train / val / test splits.

The sources below are hand-authored, not scraped. Each one carries the
facts that a correct compression must preserve, so the reward function has
ground truth to check against:

  * ``must_keep``            literal spans that must survive
  * ``must_keep_numbers``    numbers / statistics that must survive
  * ``hedges``               genuine hedges that must NOT be deleted
  * ``code_spans``           fenced code that must stay byte-for-byte

Run from the repository root::

    python skillopt-integration/scripts/build_dataset.py

The split is deterministic (fixed seed, stratified by task type), so
re-running produces identical files.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "caveman_brief_split"
SPLIT_RATIO = (6, 2, 2)  # train : val : test
SEED = 42

# ─────────────────────────────────────────────────────────────────────────────
# Sources
# ─────────────────────────────────────────────────────────────────────────────

CODE_DOCX = """from docx import Document

doc = Document()
doc.add_heading("Laporan Tahunan", level=1)
doc.add_paragraph("Ringkasan eksekutif")
doc.save("laporan.docx")
"""

CODE_GGPLOT = """library(ggplot2)

ggplot(df, aes(x = month, y = revenue)) +
  geom_col(fill = "#2C7FB8") +
  theme_minimal()
"""

CODE_PATCH = """- if token.expires_at < now:
+ if token.expires_at <= now:
"""

SOURCES: list[dict] = [
    # ── English academic prose ────────────────────────────────────────────
    {
        "key": "shipments",
        "language": "en",
        "task_type": "academic_prose",
        "instruction": "Tighten this paragraph for a report.",
        "source": (
            "It is important to note that, over the course of the observation period, "
            "a significant number of the shipments that were processed experienced delays "
            "which could possibly be attributed to a variety of different factors, "
            "including but not limited to handover procedures between shifts. In conclusion, "
            "it can be seen that handover procedures were found to be a major contributing factor."
        ),
        "must_keep": ["shipments", "delays", "handover procedures"],
        "must_keep_numbers": [],
        "hedges": [],
        "target_compression": 0.55,
    },
    {
        "key": "limitations",
        "language": "en",
        "task_type": "academic_prose",
        "instruction": "Rewrite the limitations section more concisely.",
        "source": (
            "It should be noted that the present study has a number of limitations that "
            "need to be taken into consideration when interpreting the results. First of all, "
            "the sample size was relatively small, with a total of 150 participants, and "
            "furthermore, all of the participants were recruited from a single geographic "
            "region, namely Surabaya. In addition to this, the design of the study was "
            "cross-sectional in nature, which means that it is not possible to draw any "
            "conclusions about causality. The findings may therefore not generalise to "
            "other populations."
        ),
        "must_keep": ["Surabaya", "cross-sectional"],
        "must_keep_numbers": [150],
        "hedges": ["may"],
        "target_compression": 0.55,
    },
    {
        "key": "methodology",
        "language": "en",
        "task_type": "academic_prose",
        "instruction": "Compress this methodology paragraph without losing any data.",
        "source": (
            "The purpose of this section is to describe the methodology that was employed "
            "in order to conduct the analysis. A total of 1,240 survey responses were "
            "collected over a period of six months, and after the process of data cleaning "
            "was completed, 1,087 responses were retained for the final analysis, which "
            "represents a retention rate of 87.7%. The instrument that was used was adapted "
            "from the work of Santoso and Wijaya, and it demonstrated a Cronbach's alpha "
            "of 0.89. It is worth mentioning that informed consent was obtained from each "
            "and every participant prior to their participation in the study."
        ),
        "must_keep": ["Santoso", "Wijaya", "Cronbach"],
        "must_keep_numbers": [1240, 1087, 87.7, 0.89],
        "hedges": [],
        "target_compression": 0.55,
    },
    {
        "key": "intervention",
        "language": "en",
        "task_type": "academic_prose",
        "instruction": "Tighten this results paragraph. Keep the clinical hedge.",
        "source": (
            "The results of the analysis indicate that the intervention was associated with "
            "a reduction in systolic blood pressure of approximately 6.4 mmHg, although it "
            "should be emphasised that this effect may be attributable, at least in part, to "
            "changes in concomitant medication rather than to the intervention itself. "
            "Furthermore, it is important to note that the observed difference did not reach "
            "conventional levels of statistical significance, with p = 0.07."
        ),
        "must_keep": ["systolic blood pressure"],
        "must_keep_numbers": [6.4, 0.07],
        "hedges": ["may"],
        "target_compression": 0.45,
    },

    # ── Indonesian academic prose ─────────────────────────────────────────
    {
        "key": "keterbatasan",
        "language": "id",
        "task_type": "academic_prose",
        "instruction": "Ringkas bagian keterbatasan ini tanpa kehilangan data.",
        "source": (
            "Perlu diketahui bahwa penelitian ini memiliki beberapa keterbatasan yang "
            "perlu dipertimbangkan. Pertama-tama, ukuran sampel tergolong kecil, yaitu "
            "sebanyak 150 partisipan, dan selain itu seluruh partisipan direkrut dari "
            "satu wilayah geografis, yaitu Surabaya. Di samping itu, desain penelitian "
            "bersifat potong lintang, sehingga tidak dimungkinkan untuk menarik kesimpulan "
            "mengenai hubungan sebab-akibat. Oleh karena itu, temuan mungkin tidak dapat "
            "digeneralisasi ke populasi lain."
        ),
        "must_keep": ["Surabaya", "potong lintang"],
        "must_keep_numbers": [150],
        "hedges": ["mungkin"],
        "target_compression": 0.55,
    },
    {
        "key": "metodologi-id",
        "language": "id",
        "task_type": "academic_prose",
        "instruction": "Padatkan paragraf metodologi ini. Data harus tetap utuh.",
        "source": (
            "Pada dasarnya, tujuan dari bagian ini adalah untuk menjelaskan metodologi "
            "yang digunakan dalam penelitian. Sebanyak 1.240 respons survei berhasil "
            "dikumpulkan selama periode enam bulan, dan setelah proses pembersihan data "
            "selesai dilakukan, sebanyak 1.087 respons dipertahankan untuk analisis akhir, "
            "yang mana hal ini merepresentasikan tingkat retensi sebesar 87,7%. Instrumen "
            "yang digunakan diadaptasi dari Santoso dan Wijaya dengan nilai Cronbach's "
            "alpha sebesar 0,89."
        ),
        "must_keep": ["Santoso", "Wijaya", "Cronbach"],
        "must_keep_numbers": [1240, 1087, 87.7, 0.89],
        "hedges": [],
        "target_compression": 0.55,
    },

    # ── English office prose ──────────────────────────────────────────────
    {
        "key": "status-update",
        "language": "en",
        "task_type": "office_email",
        "instruction": "Rewrite this status update as a tight internal note.",
        "source": (
            "I just wanted to take a moment to give you a quick update on where we are with "
            "the Q1 deliverables. As you may already be aware, the API work has now been "
            "completed and it currently has a test coverage of 95%. With regard to the "
            "frontend, that is still very much a work in progress, and our current estimate "
            "is that it will be ready by Friday. In terms of the budget, we are presently "
            "running under forecast. There is one risk that I would like to flag, which is "
            "that there has been a delay on the vendor side, and our proposed mitigation for "
            "this is to line up a backup supplier."
        ),
        "must_keep": ["Q1", "API"],
        "must_keep_numbers": [95],
        "hedges": [],
        "target_compression": 0.55,
    },
    {
        "key": "meeting-request",
        "language": "en",
        "task_type": "office_email",
        "instruction": "Shorten this email. Keep it polite but trim the padding.",
        "source": (
            "I hope this message finds you well. I am writing to you today because I was "
            "wondering whether you might possibly have some time available at any point "
            "during the course of next week in order for us to be able to get together and "
            "discuss the draft of the annual report. I think it would probably be a good "
            "idea if we could touch base before the submission deadline, which as you know "
            "is on the 14th of March. Please do let me know what might work best for you."
        ),
        "must_keep": ["annual report"],
        "must_keep_numbers": [14],
        "hedges": [],
        "target_compression": 0.50,
    },

    # ── Indonesian office prose ───────────────────────────────────────────
    {
        "key": "laporan-bulanan",
        "language": "id",
        "task_type": "office_email",
        "instruction": "Ringkas laporan bulanan ini menjadi catatan singkat.",
        "source": (
            "Dengan ini saya ingin menyampaikan laporan mengenai perkembangan proyek "
            "selama bulan berjalan. Perlu dicatat bahwa pekerjaan integrasi API telah "
            "selesai dilaksanakan dengan cakupan pengujian sebesar 95%. Sementara itu, "
            "untuk bagian antarmuka pengguna, pengerjaan masih berlangsung dan diperkirakan "
            "akan selesai pada hari Jumat. Dari sisi anggaran, pengeluaran saat ini masih "
            "berada di bawah perkiraan. Namun demikian, terdapat satu risiko yang perlu "
            "diwaspadai, yaitu keterlambatan dari pihak vendor."
        ),
        "must_keep": ["API"],
        "must_keep_numbers": [95],
        "hedges": [],
        "target_compression": 0.55,
    },

    # ── Code-assist tasks (code must stay byte-exact) ─────────────────────
    {
        "key": "docx-script",
        "language": "en",
        "task_type": "code_assist",
        "instruction": "Explain briefly how to generate the report file, then give the script.",
        "source": (
            "I was wondering if you could possibly help me out with a small task that I have "
            "been struggling with for quite some time now. What I am essentially trying to "
            "achieve here is to be able to generate a DOCX file that contains a heading "
            "followed by a paragraph of text, and I have been given to understand that the "
            "python-docx library would probably be the most appropriate tool for this "
            "particular purpose. The heading needs to say 'Laporan Tahunan' and the "
            "paragraph needs to say 'Ringkasan eksekutif'."
        ),
        "must_keep": ["python-docx", "Laporan Tahunan", "Ringkasan eksekutif"],
        "must_keep_numbers": [],
        "hedges": [],
        "code_spans": [CODE_DOCX],
        "target_compression": 0.50,
    },
    {
        "key": "ggplot-script",
        "language": "en",
        "task_type": "code_assist",
        "instruction": "Show the shortest working R chart call for monthly revenue.",
        "source": (
            "It is important to note that, when it comes to the visualisation of monthly "
            "revenue data, there are a great many different approaches that one could "
            "potentially take. However, in my experience, the approach that tends to work "
            "the best in the vast majority of cases is to make use of the ggplot2 package, "
            "and in particular to utilise a column geometry together with a minimal theme. "
            "The colour that we have standardised on across the organisation is #2C7FB8."
        ),
        "must_keep": ["ggplot2", "#2C7FB8"],
        "must_keep_numbers": [],
        "hedges": [],
        "code_spans": [CODE_GGPLOT],
        "target_compression": 0.55,
    },

    # ── Coding-agent replies ──────────────────────────────────────────────
    {
        "key": "react-rerender",
        "language": "en",
        "task_type": "agent_reply",
        "instruction": "Why does my React component re-render every time?",
        "source": (
            "The reason why your React component is re-rendering is likely to be because "
            "you are creating a brand new object reference on each and every render cycle. "
            "When you pass an inline object as a prop, React's shallow comparison will see "
            "it as a different object every single time, and this is what triggers the "
            "re-render. What I would recommend that you do in this situation is to use "
            "useMemo in order to memoize the object."
        ),
        "must_keep": ["useMemo", "React"],
        "must_keep_numbers": [],
        "hedges": [],
        "target_compression": 0.60,
    },
    {
        "key": "connection-pooling",
        "language": "en",
        "task_type": "agent_reply",
        "instruction": "Explain database connection pooling.",
        "source": (
            "Connection pooling is a technique whereby the system reuses connections that "
            "are already open, instead of creating a brand new connection for each and "
            "every individual request that comes in. The main reason why this is done is "
            "that it avoids the overhead that is associated with repeating the handshake "
            "process over and over again."
        ),
        "must_keep": [],
        "must_keep_numbers": [],
        "hedges": [],
        "target_compression": 0.50,
    },
    {
        "key": "auth-bug",
        "language": "en",
        "task_type": "agent_reply",
        "instruction": "My JWT refresh logs users out one second early. What is wrong?",
        "source": (
            "There is a bug that is located in the authentication middleware. The check "
            "that is performed on the token expiry is currently using a strict less-than "
            "comparison operator, when in actual fact it really ought to be using a "
            "less-than-or-equal-to comparison instead. The fix for this is shown below."
        ),
        "must_keep": ["authentication middleware", "token expiry"],
        "must_keep_numbers": [],
        "hedges": [],
        "code_spans": [CODE_PATCH],
        "target_compression": 0.50,
    },
    {
        "key": "exec-summary-id",
        "language": "id",
        "task_type": "office_email",
        "instruction": "Buat ringkasan eksekutif yang padat dari teks ini.",
        "source": (
            "Sebagai kesimpulan, dapat disimpulkan bahwa kinerja unit layanan pelanggan "
            "selama kuartal ini menunjukkan peningkatan yang cukup signifikan apabila "
            "dibandingkan dengan kuartal sebelumnya. Waktu respons rata-rata berhasil "
            "diturunkan dari 48 jam menjadi 12 jam, dan tingkat kepuasan pelanggan "
            "mengalami kenaikan sebesar 14%. Meskipun demikian, masih terdapat beberapa "
            "area yang memerlukan perhatian lebih lanjut, terutama yang berkaitan dengan "
            "proses eskalasi tiket."
        ),
        "must_keep": [],
        "must_keep_numbers": [48, 12, 14],
        "hedges": [],
        "target_compression": 0.50,
    },
]

# Which registers each task type is meaningful for.
REGISTER_BY_TASK: dict[str, list[str]] = {
    "academic_prose": ["be_brief", "unified", "grug_reasoning"],
    "office_email": ["be_brief", "unified", "grug_reasoning"],
    "code_assist": ["unified", "caveman", "grug_reasoning"],
    "agent_reply": ["unified", "caveman", "grug_reasoning"],
}

# Word budgets for the grug reasoning register mirror the skill's own budgets.
REASONING_BUDGET = {
    "agent_reply": 120,
    "code_assist": 200,
    "academic_prose": 200,
    "office_email": 160,
}


def _adjust_target_for_code(target: float, code_spans: list) -> float:
    """Lower the compression target when the answer must carry a code block.

    A required code artifact is byte-exact and uncompressible, so it inflates
    the output length no matter how tightly the prose is written. Holding a
    code-assist task to a prose-level 55% reduction would punish a perfect
    answer for the code it was required to emit.
    """
    if not code_spans:
        return target
    return min(target, 0.30)


def build_items() -> list[dict]:
    items: list[dict] = []
    for source in SOURCES:
        task_type = source["task_type"]
        for register in REGISTER_BY_TASK.get(task_type, ["be_brief"]):
            item = {
                "id": f"{source['key']}-{register.replace('_', '-')}",
                "task_type": task_type,
                "register": register,
                "language": source["language"],
                "source": source["source"],
                "instruction": source["instruction"],
                "must_keep": list(source.get("must_keep", [])),
                "must_keep_numbers": list(source.get("must_keep_numbers", [])),
                "must_keep_citations": list(source.get("must_keep_citations", [])),
                "hedges": list(source.get("hedges", [])),
                "code_spans": list(source.get("code_spans", [])),
                "target_compression": _adjust_target_for_code(
                    source.get("target_compression", 0.5), source.get("code_spans", [])
                ),
                "reasoning_budget_tokens": REASONING_BUDGET.get(task_type, 200),
            }
            # The grug register reasons internally, so it needs more headroom
            # than the visible answer alone.
            if register == "grug_reasoning":
                item["max_output_tokens"] = 700
            else:
                item["max_output_tokens"] = 400
            items.append(item)
    return items


def stratified_split(items: list[dict]) -> dict[str, list[dict]]:
    """Split train:val:test, keeping each task_type proportional in every split."""
    rng = random.Random(SEED)
    by_task: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        by_task[item["task_type"]].append(item)

    buckets: dict[str, list[dict]] = {"train": [], "val": [], "test": []}
    train_w, val_w, test_w = SPLIT_RATIO
    total_w = train_w + val_w + test_w

    for task in sorted(by_task):
        pool = list(by_task[task])
        rng.shuffle(pool)
        n = len(pool)
        n_train = max(1, round(n * train_w / total_w))
        n_val = max(1, round(n * val_w / total_w))
        n_test = max(1, n - n_train - n_val)
        buckets["train"].extend(pool[:n_train])
        buckets["val"].extend(pool[n_train:n_train + n_val])
        buckets["test"].extend(pool[n_train + n_val:n_train + n_val + n_test])

    for split in buckets:
        buckets[split].sort(key=lambda i: i["id"])
    return buckets


def main() -> None:
    items = build_items()
    splits = stratified_split(items)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, rows in splits.items():
        split_dir = OUT_DIR / name
        split_dir.mkdir(parents=True, exist_ok=True)
        (split_dir / "items.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest[name] = len(rows)

    (OUT_DIR / "split_manifest.json").write_text(
        json.dumps(
            {
                "split_mode": "manual_stratified",
                "split_seed": SEED,
                "split_ratio": "train:val:test = "
                               f"{SPLIT_RATIO[0]}:{SPLIT_RATIO[1]}:{SPLIT_RATIO[2]}",
                "counts": manifest,
                "registers": sorted({i["register"] for i in items}),
                "task_types": sorted({i["task_type"] for i in items}),
                "languages": sorted({i["language"] for i in items}),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest} to {OUT_DIR}")


if __name__ == "__main__":
    main()
