---
name: md-format
description: |
  Formats markdown using Prettier to fix broken tables, missing line breaks, and inconsistent spacing. Automatically checks for and installs Prettier if needed. Use when AI-generated markdown needs cleanup or when you see poorly formatted documentation.
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

### Step 1: Check for Prettier

Before formatting, verify Prettier is available:

```bash
if ! command -v prettier &> /dev/null; then
    npm install -g prettier
fi
```

### Step 2: Format the Markdown

Use the `prettier` CLI with the markdown parser:

```bash
# Format from stdin
echo "# Heading" | prettier --parser markdown

# Format a file in place
prettier --parser markdown --write path/to/file.md
```

### Step 3: Handle Missing Dependencies

If Prettier is not installed, the script will automatically install it using `npm install -g prettier`.

## Enhanced Features

- **Linting integration** with markdownlint-cli
- **Technical mode** for documents with equations/code (120 char lines)
- **Auto-fix mode** for CI/CD pipelines
- **Configuration support** via `.markdownlint.json` and `.prettierrc` files

## Automatic Formatting Setup

To automatically format markdown files written by the agent, set up a Claude Code hook:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.filePath // .path // empty' 2>/dev/null | grep -E '\.md$' | head -1)
if [ -n "$FILE_PATH" ] && [[ "$FILE_PATH" == *.md ]]; then
    python scripts/format_and_lint.py --fix "$FILE_PATH" 2>/dev/null || true
fi
exit 0
```

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "postWrite": [
      {
        "command": "~/.claude/hooks/pre-post.md-format",
        "match": "*.md"
      }
    ]
  }
}
```

## Triggering the Skill

The skill can be triggered in multiple ways:

1. **Direct invocation**: `/md-format` or `/md-format <file-path>`
2. **Python script**: `python scripts/format_and_lint.py <options> <files>`
3. **Prettier CLI**: `npx prettier --parser markdown <file>`
