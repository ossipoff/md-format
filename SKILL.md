---
name: md-format
description: |
  Formats and cleans up markdown documents — fixes broken tables, missing line breaks, inconsistent spacing, trailing punctuation, and other common issues. Automatically installs both tools globally if needed. Use when AI-generated markdown needs cleanup, documentation looks messy, or you want to fix formatting in any .md file.
keywords:
  - markdown
  - md
  - document
  - docs
  - doc
  - text
  - table
  - alignment
  - broken
  - messy
  - format
  - formatting
  - tidy
  - clean
  - style
  - consistent
  - whitespace
  - spacing
  - readable
  - prettify
  - pretty
  - improve
  - enhance
  - write
  - writing
  - documentation
  - heading
  - list
  - code block
  - blank line
  - indentation
  - paragraph
compatibility: claude-code opencode
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# md-format: Markdown Formatter

Formats markdown content to fix common issues like broken tables, missing line breaks, and inconsistent spacing.

**IMPORTANT:** Always use `python scripts/format_and_lint.py` (or `/md-format`) as your entry point. Never invoke prettier or markdownlint directly — they are implementation details hidden behind this script.

## When to Use

Use this skill when:
- AI generates markdown with broken tables
- You see missing blank lines in markdown output
- Markdown looks "squished" or hard to read

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python scripts/format_and_lint.py file.md` | Check formatting |
| `python scripts/format_and_lint.py --fix file.md` | Auto-fix issues |
| `python scripts/format_and_lint.py --dry-run file.md` | Preview changes |

## Workflow

1. **Identify the input** - Determine if you have raw markdown text or a file path
2. **Run the script** - Execute `python scripts/format_and_lint.py <options> <files>` — this is the only supported entry point
3. **Verify results** - Check that formatting was applied correctly

### Correct vs Incorrect Approaches

```
CORRECT:                          WRONG:
python scripts/...               npx prettier ...
/md-format                       npx markdownlint-cli ...
                                 direct tool invocation
```

## Examples

### Fix Broken Table Alignment

**Before:**
```markdown
|Name|Age|City|
|---|---|---|
|John|25|NYC|
```

**After:**
```markdown
| Name | Age | City |
| ---- | --- | ---- |
| John | 25  | NYC  |
```

### Add Missing Line Breaks

**Before:**
```markdown
# Heading## Subheading

- Item 1
```

**After:**
```markdown
# Heading

## Subheading

- Item 1
```

## Implementation

The script handles everything automatically:

1. Checks for required tools and installs them globally if needed (with npx fallback)
2. Applies Prettier formatting with markdown parser
3. Runs markdownlint checks and auto-fixes when `--fix` is used

### Supported Options

| Flag | Description |
|------|-------------|
| (none) | Check mode — shows what needs fixing without modifying files |
| `--fix` | Auto-fix both formatting and linting issues |
| `--dry-run` | Preview changes without applying them |
| `--technical` | Relaxed line length (120 chars) for code/equations |
| `--print-width N` | Custom line length |
| `--no-lint` | Skip linting step |
| `--no-format` | Skip formatting step |

## Enhanced Features

- **Linting integration** with markdownlint-cli (via the script)
- **Technical mode** for documents with equations/code (120 char lines)
- **Auto-fix mode** for CI/CD pipelines
- **Configuration support** via `.markdownlint.json` and `.prettierrc` files

## Setup Instructions

For automatic formatting setup instructions, see the [README.md](README.md) file.

## Triggering the Skill

The skill can be triggered in multiple ways:

1. **Direct invocation**: `/md-format` or `/md-format <file-path>`
2. **Python script**: `python scripts/format_and_lint.py <options> <files>`
