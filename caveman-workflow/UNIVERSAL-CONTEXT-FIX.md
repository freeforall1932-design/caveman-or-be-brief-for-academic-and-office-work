# Universal Context Fix Applied

## Summary
All specific names, dates, numbers, and locations replaced with universal placeholders to ensure adaptability across any country, institution, or document type.

## Replacements Made

| Original Pattern | Universal Placeholder | Use Case |
|-----------------|----------------------|----------|
| n=45, n=30 | n=[SAMPLE_SIZE], n=[NUMBER] | Academic sample sizes |
| Q4, Q3 | Q[QUARTER] | Quarterly reports |
| Dec 15, Friday | [DATE] | Deadlines, dates |
| 95%, 8%, 18% | [PERCENTAGE]% | Metrics, statistics |
| $12.4M, $5.1M | $[AMOUNT] | Financial figures |
| 2020, 2023 | [YEAR] | Citations, years |
| Smith et al. | Author et al. | Citation examples |
| Stanford, IEEE | [Institution], [Publisher] | Names of entities |
| Project Alpha | [Project Name] | Office project names |
| Thesis_Draft_v2.pdf | [File Name] | Document references |

## Files Updated

### Skills Directory
- `skills/caveman.md` — Main skill definition
- `skills/caveman-compress.md` — Document compression skill
- `skills/caveman-review.md` — Review feedback skill

### Custom Instructions
- `custom-instructions/claude-instructions.md` — Claude-specific setup
- `custom-instructions/qwen-instructions.md` — Qwen-specific setup

### CLI Scripts
- `cli-scripts/claude-cli.sh` — Claude command-line interface
- `cli-scripts/qwen-cli.sh` — Qwen command-line interface

### Documentation
- `README.md` — Main documentation
- `VERIFICATION-REPORT.md` — Test results (examples updated)
- `debug-test.md` — Debug test cases (examples updated)

## Usage Example

Before (non-universal):
```
"Study limitations: sample size small (n=45), single geographic region...
Q4 deliverables on track. Backend API complete (95% test coverage).
Frontend integration in progress, ETA Dec 15."
```

After (universal):
```
"Study limitations: sample size small (n=[SAMPLE_SIZE]), single geographic region...
Q[QUARTER] deliverables on track. Backend API complete ([PERCENTAGE]% test coverage).
Frontend integration in progress, ETA [DATE]."
```

## Benefits

1. **Universally Adaptable**: Works for any country, institution, or document
2. **Template-Ready**: Users can directly copy and fill placeholders
3. **No Confusion**: Clear distinction between example and actual content
4. **Consistent Format**: Same placeholder style across all files

## How to Use

When using caveman workflow:
1. Replace `[PLACEHOLDER]` with your actual values
2. Or let AI auto-fill based on your document context
3. Placeholders signal "insert your specific data here"

Example prompt:
```
"/caveman full — draft limitations section with n=[SAMPLE_SIZE]=120, 
[PERCENTAGE]=87, [YEAR]=2024"
```

AI output:
```
"Study limitations: sample size moderate (n=120), single geographic region...
Achieved 87% response rate. Data collected in 2024."
```
