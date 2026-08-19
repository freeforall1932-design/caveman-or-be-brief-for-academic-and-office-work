# Ralph Wiggum Loop — Iterative Self-Improvement (Optional)

*"Why use many token when few token do trick — but what if few token not quite right?"*

## What Is It?

The Ralph Wiggum loop is a pattern where an AI agent repeatedly processes the same prompt, improving its output with each iteration. Progress lives in files and git history, not context windows — so each fresh iteration starts with a clear, unfilled context.

```bash
while :; do cat PROMPT.md | agent ; done
```

## When to Use

### ✅ TURN ON (ralph on)
- You have time and tokens to spare
- Quality is critical (final thesis chapter, journal submission)
- Complex multi-step document assembly
- "I need this polished, not just fast"

### ❌ TURN OFF (ralph off)
- Deadline is tight, tokens are scarce
- Quick draft or summary is sufficient
- Casual internal notes
- "I want it fast, I don't have tokens to burn"

### ⚡ ONE-SHOT MODE (ralph once)
- Run one verification pass only
- "Double-check my output once, then stop"
- Gives you a safety net without full looping cost

## How It Works with This Project

### Integration with Grug Reasoning

The Grug engine (`claude-reasoning-caveman.skill`) handles the **internal thinking** — planning, fear assessment, tool selection. The Ralph Wiggum loop handles the **external iteration** — repeating the task with fresh context each pass.

```
[User Prompt]
    ↓
[Grug Thinks: sniff → fear → plan → act → speak]
    ↓
[Output v1] ──→ [Ralph Loop Active?] ──No──→ [Done]
    ↓ Yes
[Save output, reset context]
    ↓
[Grug Reviews Previous Output]
    ↓
[Output v2 (improved)]
    ↓
[Repeat until quality threshold or max loops]
```

### Commands

| Command | Effect |
|---------|--------|
| `ralph on` | Enable iterative loop. Will repeat task until you stop. |
| `ralph off` | Disable loop. One pass only, speed priority. |
| `ralph once` | Run one verification pass after initial output. |
| `ralph max N` | Set maximum N iterations (e.g., `ralph max 3`). |
| `ralph status` | Show current iteration count and estimated tokens used. |

### Example: Thesis Abstract Refinement

```
User: "ralph on — compress this thesis abstract for submission"

[Pass 1] → "Methodology: n=150 participants... Results: significant correlation..."
[Pass 2] → "Methodology (2024): n=150. Survey + interview. Results: X correlates Y (p<0.05)."
[Pass 3] → "Mixed-methods study (2024). Survey (n=150) + follow-up interviews (n=15). 
             Key finding: X predicts Y (β=0.42, p<0.01). Mediation by Z."
[User: "Good. ralph off."]
[Done, pass 3 kept.]
```

### Example: One-Shot Verification

```
User: "ralph once — review this email before I send it"

[Pass 1] → "L3: 🔴 typo: 'recieve' → 'receive'. L7: 🟡 risk: deadline missing timezone."
[Pass 2 (verification)] → "L3 fix confirmed. L7: Add 'EOD PST'. No new issues."
[Done, two passes complete.]
```

## Technical Note

Ralph Wiggum loop works best when:
1. Each pass starts fresh (no accumulated context)
2. Progress is saved to files between passes
3. Grug reasoning guides what to improve each iteration
4. You set a max loop count to prevent infinite token burn

## Community Resources

- Anthropic official plugin: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum
- Community streamlined version: https://github.com/severity1/this-little-wiggy
- Original concept by Geoffrey Huntley

---

*Ralph Wiggum loop: optional. Use when quality matters. Skip when speed matters.*