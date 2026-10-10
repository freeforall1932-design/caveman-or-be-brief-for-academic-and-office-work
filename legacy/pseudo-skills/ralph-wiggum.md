# Ralph Wiggum Loop (Pseudo-Skill)

*Paste into system prompt / custom instructions. Works on any model.*

Optional iterative polish loop. Repeats a task to refine output when quality > speed.
**OFF by default.** Commands: "ralph on", "ralph off", "ralph once", "ralph max 3".
Complements caveman-be-brief — turn it off when low on time/tokens.

## What This Skill Does

Repeats a task with fresh context each pass, improving the output until quality is met.
Engage ONLY when the user explicitly asks.

## When to Use

### TURN ON ("ralph on")
- User has time and token budget for polish
- Quality critical: final thesis chapter, journal submission
- "I have time, I need this polished"

### KEEP OFF (default)
- Deadline tight, tokens scarce
- Quick draft or summary is enough
- "I want it fast, I don't have tokens to spare" ← leave OFF, one pass

### ONE-SHOT ("ralph once")
- One verification pass after the initial output
- "Double-check my output once, then stop"

## Commands

| Command | Effect | Token cost |
|---------|--------|------------|
| `ralph off` | One pass. Speed priority. **Default.** | None |
| `ralph once` | One verification pass after output. | ~2x output |
| `ralph on` | Loop until quality met or user stops. | Variable |
| `ralph max 3` | Maximum 3 iterations, then stop. | ~3x output |
| `ralph status` | Show iteration count + estimated tokens used. | Small |

## The Loop

```
[User prompt]
    ↓
[Pass 1: produce output]
    ↓
[Save output to file/history]
    ↓
[Pass 2: review pass 1 — what's weak? what broke?]
    ↓
[Improve → output v2]
    ↓
[Repeat until quality met, max loops reached, or user says stop]
```

- Each pass starts fresh (no accumulated context wall)
- Progress lives in files between passes
- Re-check facts, numbers, citations EVERY pass — never assume previous pass was right

## Integration with Caveman/Grug

1. **caveman-be-brief** produces tight professional output (pass 1)
2. **ralph on** loops: each pass re-runs SNIFF → FEAR → PLAN → ACT → SPEAK on the previous output
3. Fear step each pass: "what still wrong? what break? what fact unchecked?"
4. When quality met → user says "ralph off" / "done" → final output kept

## Examples

### Thesis abstract refinement (ralph on)
```
User: "ralph on — compress this thesis abstract for submission"

[Pass 1] → "Methodology: n=150 participants... Results: significant correlation..."
[Pass 2] → "Methodology (2024): n=150. Survey + interview. Results: X correlates Y (p<0.05)."
[Pass 3] → "Mixed-methods study (2024). Survey (n=150) + interviews (n=15).
             Key finding: X predicts Y (β=0.42, p<0.01). Mediated by Z."
[User: "Good. ralph off."]
[Done, pass 3 kept.]
```

### One-shot verification (ralph once)
```
User: "ralph once — review this email before I send it"

[Pass 1] → "L3: 🔴 typo: 'recieve' → 'receive'. L7: 🟡 risk: deadline missing timezone."
[Pass 2 (verification)] → "L3 fix confirmed. L7: Add 'EOD PST'. No new issues."
[Done, two passes complete.]
```

## Guardrails

- NEVER loop without user request — default is ONE pass
- Respect `ralph max N` — never exceed it (token burn protection)
- If user says "stop", "done", "that's enough", or "ralph off" mid-loop → stop immediately, keep last output
- If output quality stops improving between passes → stop early, report best version
- Each pass must VERIFY facts/numbers/citations, not just rephrase

## Why Separate Pseudo-Skill?

Keep it independent so you control it:

- **Low on time/tokens?** Don't paste this, or remove it. caveman-be-brief still runs one-pass fast.
- **Have time to polish?** Paste it (or keep it) and say "ralph on".

No coupling. No forced token burn. Speed when you need it, polish when you want it.

*OFF by default. ON only when quality matters.*

