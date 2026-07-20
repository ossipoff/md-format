---
name: md-format
description: |
  Formats markdown using Prettier and linting with markdownlint-cli to fix broken tables, missing line breaks, and inconsistent spacing. Automatically installs both tools globally if needed. Use when AI-generated markdown needs cleanup or when you see poorly formatted documentation.
keywords:
  - markdown
  - md
  - document
  - note
  - text
  - table
  - alignment
  - broken
  - messy
compatibility: claude-code opencode
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# md-format: Markdown Formatter

Formats markdown content using Prettier to fix common issues like broken tables, missing line breaks, and inconsistent spacing.

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
2. **Choose the method** - Use appropriate approach based on input type
3. **Format with the skill** - Run `python scripts/format_and_lint.py` (not direct prettier)
4. **Verify results** - Check that formatting was applied correctly

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

### Step 1: Check for Tools

The script automatically checks for both Prettier and markdownlint-cli and installs them globally if needed. It also has npx fallback if global installation fails.

### Step 2: Format and Lint the Markdown

Use the Python script which handles both formatting and linting:

```bash
# Format and lint a file (check mode)
python scripts/format_and_lint.py path/to/file.md

# Auto-fix issues (both Prettier formatting and markdownlint fixes)
python scripts/format_and_lint.py --fix path/to/file.md
```

### Step 3: How It Works

The script:
1. Checks if Prettier is installed globally, installs if needed
2. Checks if markdownlint-cli is installed globally, installs if needed
3. Falls back to npx if global installation fails
4. Applies Prettier formatting with markdown parser
5. Runs markdownlint checks and auto-fixes when --fix is used

## Enhanced Features

- **Linting integration** with markdownlint-cli
- **Technical mode** for documents with equations/code (120 char lines)
- **Auto-fix mode** for CI/CD pipelines
- **Configuration support** via `.markdownlint.json` and `.prettierrc` files

## Setup Instructions

For automatic formatting setup instructions, see the [README.md](README.md) file.

## Triggering the Skill

The skill can be triggered in multiple ways:

1. **Direct invocation**: `/md-format` or `/md-format <file-path>`
2. **Python script**: `python scripts/format_and_lint.py <options> <files>`