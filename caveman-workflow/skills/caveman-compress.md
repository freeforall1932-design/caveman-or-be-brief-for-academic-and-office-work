# Caveman Compress Skill

**Source:** Adapted from JuliusBrussee/caveman repository  
**Purpose:** Compress existing documents to save input tokens (~46% savings)

---

## Skill Definition

```yaml
name: caveman-compress-academic-office
description: >
  Compress natural language documents (thesis notes, research summaries, reports)
  into token-efficient format. Preserves all technical substance, citations, code.
  Backup saved as FILE.original.md before overwriting.
  Trigger: "/caveman-compress FILEPATH" or "compress this document"

supported_formats:
  compress: [".md", ".txt", ".typ", ".tex", ".typst"]
  skip: [".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".env", ".css", ".html"]

process:
  step1: "Detect file type (no tokens)"
  step2: "Create backup: FILE.original.md"
  step3: "Compress prose sections only"
  step4: "Preserve code blocks exactly"
  step5: "Overwrite original with compressed version"
  step6: "Report compression ratio to user"

compression_rules:
  remove:
    - articles: ["a", "an", "the"]
    - filler: ["just", "really", "basically", "actually", "simply", "essentially", "generally"]
    - pleasantries: ["sure", "certainly", "of course", "happy to", "I'd recommend"]
    - hedging: ["it might be worth", "you could consider", "it would be good to"]
    - redundant_phrases:
        "in order to": "to"
        "make sure to": "ensure"
        "the reason is because": "because"
        "due to the fact that": "because"
    - connective_fluff: ["however", "furthermore", "additionally", "in addition"]

  preserve_exact:
    - code_blocks: "Everything inside ``` ... ```"
    - inline_code: "Everything inside `backticks`"
    - urls: "Full URLs, markdown links"
    - file_paths: "/src/components/..., ./config.yaml"
    - commands: "npm install, git commit, docker build"
    - technical_terms: "Library names, API names, protocols, algorithms"
    - proper_nouns: "Project names, people, companies"
    - numeric_values: "Dates, version numbers, statistics"
    - environment_variables: "$HOME, NODE_ENV"
    - citations: "APA, MLA, Chicago, IEEE, BibTeX entries"
    - equations: "LaTeX math, formulas"

  preserve_structure:
    - headings: "Keep exact heading text"
    - bullet_hierarchy: "Maintain nesting levels"
    - numbered_lists: "Keep numbering"
    - tables: "Compress cell text, keep structure"
    - frontmatter: "YAML headers in markdown"

  compress_strategy:
    - short_synonyms: '"big" not "extensive", "fix" not "implement a solution for"'
    - fragments_ok: '"Run tests before commit" not "You should always run tests..."'
    - drop_should: 'Remove "you should", "make sure to", "remember to"'
    - merge_redundant: "Combine bullets saying same thing differently"
    - one_example: "Keep one example where multiple show same pattern"

critical_rules:
  - "Anything inside ``` ... ``` must be copied EXACTLY"
  - "Do not remove comments, spacing, reorder lines in code"
  - "Inline code (`...`) preserved EXACTLY"
  - "If mixed content (prose + code), compress ONLY prose"
  - "If unsure whether code or prose, leave unchanged"
  - "Never compress FILE.original.md (skip it)"

examples:
  paragraph_compression:
    original: |
      You should always make sure to run the test suite before pushing any 
      changes to the main branch. This is important because it helps catch 
      bugs early and prevents broken builds from being deployed to production.
    compressed: |
      Run tests before push to main. Catch bugs early, prevent broken prod deploys.

  technical_explanation:
    original: |
      The application uses a microservices architecture with the following 
      components. The API gateway handles all incoming requests and routes 
      them to the appropriate service. The authentication service is 
      responsible for managing user sessions and JWT tokens.
    compressed: |
      Microservices architecture. API gateway route all requests to services. 
      Auth service manage user sessions + JWT tokens.

  academic_abstract:
    original: |
      In this paper, we propose a novel approach to address the problem of 
      data scarcity in machine learning applications. Our method leverages 
      transfer learning techniques to effectively utilize pre-trained models 
      on related tasks, thereby reducing the amount of labeled data required.
    compressed: |
      Paper proposes novel approach for data scarcity in ML. Method leverages 
      transfer learning to utilize pre-trained models on related tasks, 
      reducing labeled data requirements.

  thesis_methodology:
    original: |
      The research methodology employed in this study follows a quantitative 
      approach, utilizing statistical analysis to examine the relationship 
      between variables. Data was collected through structured surveys 
      administered to participants across three geographic regions over a 
      period of six months.
    compressed: |
      Research methodology: quantitative approach. Statistical analysis examine 
      variable relationships. Data collected via structured surveys to 
      participants across 3 regions over 6 months.

workflow_integration:
  docx_pdf_review:
    step1: "pandoc document.docx -o document.md"
    step2: "python3 -m scripts document.md"
    step3: "AI reviews compressed version (saves input tokens)"
    step4: "Apply fixes to original DOCX/PDF using line numbers"

  research_notes:
    step1: "Write notes normally"
    step2: "Before AI session: compress notes"
    step3: "Feed compressed notes to AI"
    step4: "Keep original for reference"

  thesis_drafting:
    step1: "Draft chapter in markdown"
    step2: "Compress for AI review"
    step3: "Get feedback on compressed version"
    step4: "Apply edits to original draft"

commands:
  compress_file: "/caveman-compress <filepath>"
  compress_cwd: "python3 -m scripts /absolute/path/to/file.md"
  check_ratio: "Reports tokens saved after compression"

expected_savings:
  input_tokens: "~46% reduction"
  output_tokens: "~65% reduction (with caveman mode)"
  combined: "Significant cost savings for long documents"
```

---

## Usage Examples

### Compress Research Notes

```bash
# Before feeding notes to AI
python3 -m scripts /home/user/research/thesis-notes.md

# Output:
# Backup saved: thesis-notes.original.md
# Compressed: 12,450 → 6,723 tokens (46% savings)
```

### Workflow with DOCX

```bash
# Step 1: Convert DOCX to Markdown
pandoc quarterly-report.docx -o quarterly-report.md

# Step 2: Compress for AI review
python3 -m scripts /workspace/quarterly-report.md

# Step 3: Ask AI for review
User: "Review quarterly-report.md for errors and improvements"

# Step 4: AI returns line-numbered feedback
AI: "L23: 🔴 bug: Q2 figure incorrect. Should be $2.4M not $2.1M.
     L45: 🟡 risk: section transition abrupt. Add bridging sentence.
     L88: 🔵 nit: inconsistent date format. Use YYYY-MM-DD."

# Step 5: Apply fixes in original Word document
```

### Batch Compression

```bash
# Compress all markdown files in directory
for file in docs/*.md; do
  python3 -m scripts $(realpath $file)
done
```

---

## Integration Notes

**For AI Agent Platforms:**
- Detect `.md`, `.txt` files in workspace
- Offer compression before large file operations
- Show token savings estimate

**For Custom Instructions:**
- Add compression workflow to model capabilities
- Explain when to use vs. when to skip

**For CLI Usage:**
- Script located in `cli-scripts/`
- Requires Python 3.8+
- Uses model API for compression
