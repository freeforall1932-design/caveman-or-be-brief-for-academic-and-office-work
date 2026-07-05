# Caveman Review Skill

**Source:** Adapted from JuliusBrussee/caveman repository  
**Purpose:** Ultra-compressed review comments for code, documents, thesis, reports

---

## Skill Definition

```yaml
name: caveman-review-academic-office
description: >
  One-line review comments for PRs, documents, thesis chapters, reports.
  Format: L<line>: <severity> <problem>. <fix>.
  Cuts review noise while preserving actionable signal.
  Trigger: "review this", "/caveman-review", "code review", "document feedback"

output_format:
  pattern: "L<line>: <severity> <problem>. <fix>."
  multiline_pattern: "L<start>-<end>: <severity> <problem>. <fix>."
  file_prefix: "<filename>:L<line>: ..."  # For multi-file diffs

severity_prefixes:
  bug:
    emoji: "🔴"
    meaning: "Critical error, will cause failure"
    use_for:
      - Broken logic
      - Missing citations
      - Undefined terms
      - Factual errors
      - Security vulnerabilities
    example: "L42: 🔴 bug: citation missing for claim. Add [Author et al., [YEAR]]."

  risk:
    emoji: "🟡"
    meaning: "Works but fragile, potential issue"
    use_for:
      - Race conditions
      - Missing null checks
      - Swallowed errors
      - Unclear transitions
      - Edge cases not handled
    example: "L88: 🟡 risk: no retry on API timeout. Add withBackoff(3)."

  nit:
    emoji: "🔵"
    meaning: "Style preference, optional fix"
    use_for:
      - Naming conventions
      - Formatting inconsistencies
      - Minor optimizations
      - Passive voice
      - Word choice
    example: "L15: 🔵 nit: inconsistent tense. Use past tense for methods."

  question:
    emoji: "❓"
    meaning: "Genuine question, not a suggestion"
    use_for:
      - Clarification needed
      - Rationale unclear
      - Alternative approaches
      - Missing context
    example: "L203: ❓ q: why exclude studies before [YEAR]?"

rules:
  remove:
    - throat_clearers: "I noticed that...", "It seems like..."
    - suggestions_framing: "You might want to consider..."
    - hedging: "perhaps", "maybe", "I think"  # Use q: instead
    - praise_in_comments: "Great work!", "Looks good but..."  # Say once at top
    - restating_code: "This line does X..."  # Reviewer can read
    - vague_feedback: "Consider refactoring this"

  preserve_exact:
    - line_numbers: "Always include exact line numbers"
    - symbol_names: "Use backticks for `functionName`, `variable`"
    - concrete_fixes: "Specific action, not general advice"
    - the_why: "If fix isn't obvious from problem"

  drop_caveman_for:
    - security_findings: "CVE-class bugs need full explanation + reference"
    - architectural_disagreements: "Need rationale, not one-liner"
    - onboarding_contexts: "New authors need the 'why'"
    - complex_multi_step_fixes: "Fragments may cause confusion"

examples:
  code_review:
    - original: |
        "I noticed that on line 42 you're not checking if the user object 
         is null before accessing the email property. This could potentially 
         cause a crash if the user is not found in the database. You might 
         want to add a null check here."
      compressed: "L42: 🔴 bug: user can be null after .find(). Add guard before .email."

    - original: |
        "It looks like this function is doing a lot of things and might 
         benefit from being broken up into smaller functions for readability."
      compressed: "L88-140: 🔵 nit: 50-line fn does 4 things. Extract validate/normalize/persist."

    - original: |
        "Have you considered what happens if the API returns a 429? I think 
         we should probably handle that case."
      compressed: "L23: 🟡 risk: no retry on 429. Wrap in withBackoff(3)."

  thesis_review:
    - original: |
        "On page 15, you mention the term 'heteroskedasticity' without 
         defining it first. Readers who aren't familiar with econometrics 
         might not understand what this means. Consider adding a definition 
         or a brief explanation when you first introduce the term."
      compressed: "P15/L42: 🔴 bug: undefined term 'heteroskedasticity'. Define on first use."

    - original: |
        "The transition between section 3.2 and 3.3 feels a bit abrupt. 
         It might help to add a sentence or two that connects these two 
         ideas more smoothly for the reader."
      compressed: "L88-95: 🟡 risk: section transition abrupt. Add bridging sentence."

    - original: |
        "Throughout the methodology section, you've been using present 
         tense, but the standard convention for describing completed 
         research is to use past tense. You may want to go through and 
         change the verb tenses accordingly."
      compressed: "L120-180: 🔵 nit: inconsistent tense. Use past tense for methods."

  document_review:
    - original: |
        "Figure 3 on page 5 doesn't have a caption. Adding a descriptive 
         title would help readers understand what the chart is showing 
         without having to refer back to the main text."
      compressed: "P5/Fig3: 🔴 bug: missing caption. Add descriptive title explaining content."

    - original: |
        "The executive summary mentions Q[QUARTER] results but the numbers don't 
         match what's in the detailed financial section. You should double- 
         check these figures to make sure they're consistent throughout 
         the document."
      compressed: "Exec Summary vs §4: 🔴 bug: Q[QUARTER] figures mismatch. Reconcile $2.4M vs $2.1M."

  office_report:
    - original: |
        "In the recommendations section, you suggest implementing a new 
         CRM system but there's no cost analysis or timeline estimate. 
         Stakeholders will need this information to make a decision."
      compressed: "§5 Recommendations: 🟡 risk: CRM proposal lacks cost/timeline. Add budget estimate + rollout schedule."

use_cases:
  academic:
    - Thesis chapter reviews
    - Journal article feedback
    - Peer review comments
    - Dissertation corrections
    - Research paper edits

  office:
    - Report quality checks
    - Presentation slide reviews
    - Policy document edits
    - Email draft feedback
    - Proposal evaluations

  code:
    - Pull request reviews
    - Code quality audits
    - Bug triage comments
    - Architecture feedback
    - Documentation reviews

commands:
  activate: "/caveman-review"
  trigger_phrases:
    - "review this PR"
    - "code review"
    - "review the diff"
    - "feedback on this chapter"
    - "check this document for errors"
  deactivate: "stop caveman-review / normal mode"

boundaries:
  does_not:
    - "Write code fixes"
    - "Approve/reject PRs"
    - "Run linters or tests"
    - "Make changes directly"
  does:
    - "Output comments ready to paste"
    - "Include line numbers"
    - "Prioritize by severity"
    - "Explain the 'why' when needed"
```

---

## Usage Examples

### Thesis Chapter Review

```
User: "Review chapter 4 for clarity and errors"

AI:
L15: 🔴 bug: undefined acronym "SEM". Define "structural equation modeling (SEM)".
L42: 🟡 risk: paragraph 8 lines, single idea. Split into 2 paragraphs.
L67: 🔵 nit: Figure 4.2 referenced before introduction. Move reference after Fig 4.2 first appears.
L88-95: 🟡 risk: transition from qualitative to quantitative abrupt. Add bridging sentence.
L120: 🔵 nit: passive voice throughout. Prefer active: "We analyzed" not "was analyzed".
L156: ❓ q: why exclude outliers >3 SD? Standard is >2.5 or robust method.
L203: 🔴 bug: citation format inconsistent. Use APA 7th throughout (Author, Year).
L245: 🟡 risk: conclusion claims causality but study correlational. Temper language.
```

### DOCX/PDF Review Workflow

```bash
# Step 1: Convert to Markdown
pandoc report.docx -o report.md

# Step 2: Request review
User: "Review report.md for errors"

# Step 3: AI returns fix list
AI:
L23: 🔴 bug: Table 2 totals don't sum. Recalculate: 45+67+89=201 not 200.
L45: 🔵 nit: date format inconsistent. Use YYYY-MM-DD not MM/DD/YYYY.
L67: 🟡 risk: section 3.1 references Appendix B but none exists. Add or remove reference.
L89: 🔴 bug: typo in company name. "Acme Corp" not "Acme Corp".
L112: ❓ q: source for industry benchmark figure 15.2%?

# Step 4: Apply fixes in Word using line numbers as guide
```

### Pull Request Review

```
User: "Review this PR diff"

AI:
src/auth.py:L34: 🔴 bug: password stored in plain text. Hash with bcrypt before save.
src/auth.py:L67: 🟡 risk: no rate limiting on login endpoint. Add throttle(5/min).
src/utils.py:L12: 🔵 nit: unused import `datetime`. Remove or use.
tests/test_auth.py:L45: ❓ q: why assert 200 not 201 for POST /register?
README.md:L88: 🔵 nit: installation steps outdated. Update npm → yarn.
```

### Office Email Draft Review

```
User: "Review this email before sending"

AI:
L3: 🔵 nit: tone too formal for internal team. "Hi all" not "Dear Team Members".
L7: 🟡 risk: deadline mentioned but no timezone. Specify "EOD PST".
L12: 🔴 bug: attachment referenced but not included. Attach Q[QUARTER]_metrics.xlsx.
L15: 🔵 nit: sign-off too abrupt. Add "Thanks" or "Best" before name.
```

---

## Integration Notes

**For AI Agent Platforms:**
- Detect review requests automatically
- Parse diff/document and return formatted comments
- Support multi-file review with filename prefix

**For Custom Instructions:**
- Add review format to model capabilities
- Explain severity prefixes to users
- Show example outputs

**For CLI Usage:**
- See `cli-scripts/` for automated review scripts
- Integrate with git hooks for pre-commit reviews
- Batch process multiple documents

---

## Best Practices

### When to Use Full Paragraphs Instead

Drop terse mode and write normal paragraphs for:

1. **Security Vulnerabilities**
   ```
   CVE-2024-XXXX requires immediate attention. This SQL injection 
   vulnerability allows authenticated users to access any record in 
   the database via crafted input to the search endpoint. 
  
   Reference: https://owasp.org/www-community/attacks/SQL_Injection
   Fix: Use parameterized queries (PreparedStatement in Java, 
   parameter binding in Python).
   ```

2. **Architectural Disagreements**
   ```
   I recommend against using microservices here because:
   - Team size (3 devs) too small for distributed system overhead
   - Deployment complexity outweighs scalability benefits at current scale
   - Data consistency challenges across service boundaries
   
   Consider modular monolith instead, refactor to services at 10x scale.
   ```

3. **Onboarding New Contributors**
   ```
   Welcome to the project! A few notes on our code style:
   
   We use TypeScript strict mode, so all functions need explicit 
   return types. This helps catch bugs early and improves IDE support.
   
   For testing, we follow AAA pattern (Arrange-Act-Assert). See 
   existing tests in /tests for examples.
   ```

### Severity Guidelines

| Severity | Response Time | Example |
|----------|--------------|---------|
| 🔴 bug | Fix before merge/submit | Missing citation, broken logic, security flaw |
| 🟡 risk | Fix if time, document if not | Edge case, potential race condition |
| 🔵 nit | Optional, author discretion | Style, naming, minor optimization |
| ❓ q | Answer for clarity | Why this approach, missing context |
