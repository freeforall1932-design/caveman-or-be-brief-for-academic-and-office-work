# Contributing to Caveman Universal

## How to Contribute

### 1. Report Issues
Use issue tracker for:
- Bugs in compression logic
- Missing language support
- Citation/LaTeX preservation failures
- CLI script errors

### 2. Submit Changes
1. Create a branch: `git checkout -b feature/your-feature`
2. Test with real documents (thesis, reports, PDFs)
3. Include benchmark results (token savings %)
4. Submit with clear description

### 3. Testing Requirements
- Test with at least 3 document types (academic, office, technical)
- Verify 100% data preservation (names, numbers, citations)
- Confirm context mismatch warning triggers correctly
- Check universal placeholders work (`[YEAR]`, `[AUTHOR]`, etc.)

## Code Style
- Markdown files: Use YAML frontmatter for skills
- Shell scripts: POSIX-compatible, no bash-specific features unless required
- Examples: Use universal placeholders, no specific names/dates

## License
Contributions fall under the MIT License.
