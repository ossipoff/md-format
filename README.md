# md-format Skill

A Claude Code skill for formatting markdown using Prettier with integrated linting.

## Quick Start

```bash
# Format from stdin (check mode - no changes)
echo "# Heading" | python scripts/format_and_lint.py

# Format a file (check mode - shows what needs fixing)
python scripts/format_and_lint.py path/to/file.md

# Auto-fix and write changes
python scripts/format_and_lint.py --fix path/to/file.md

# Dry run to see changes without modifying
python scripts/format_and_lint.py --dry-run path/to/file.md
```

## Installation

The skill is located at `/home/doj/.claude/skills/md-format/`.

## Usage

### Via Bash (direct prettier command)

```bash
# Format from stdin
echo "# Heading" | prettier --parser markdown

# Format a file in place
prettier --parser markdown --write path/to/file.md

# Format and save to output
prettier --parser markdown path/to/input.md > path/to/output.md
```

### Via Python script (Enhanced)

```bash
# Format from stdin (check mode - shows what needs fixing)
echo "# Heading" | python scripts/format_and_lint.py

# Format a file (check mode - shows what needs fixing)
python scripts/format_and_lint.py path/to/file.md

# Auto-fix and write changes
python scripts/format_and_lint.py --fix path/to/file.md

# Dry run to see changes without modifying
python scripts/format_and_lint.py --dry-run path/to/file.md

# Technical mode for docs with equations/code (120 char lines)
python scripts/format_and_lint.py --technical path/to/file.md

# Custom print width
python scripts/format_and_lint.py --print-width 100 path/to/file.md

# CI mode (exit code 1 on issues)
python scripts/format_and_lint.py --ci path/to/file.md

# Skip linting, format only
python scripts/format_and_lint.py --no-lint path/to/file.md

# Write changes explicitly
python scripts/format_and_lint.py --write path/to/file.md

# Fix both Prettier formatting and markdownlint issues
python scripts/format_and_lint.py --fix path/to/file.md
```

## Features

- **Check-by-default**: Safe default - shows what needs fixing without modifying files
- **Auto-installation**: Automatically installs Prettier if not found
- **Table formatting**: Properly aligns markdown tables with consistent spacing
- **Line break fixing**: Adds missing blank lines between elements
- **Heading consistency**: Ensures proper spacing around headings
- **List formatting**: Formats ordered and unordered lists correctly
- **Linting integration**: Validates against markdownlint rules
- **Technical mode**: Relaxed 120-char line length for code/equations
- **Dry-run mode**: Preview changes before applying
- **Custom print width**: Specify any line length with --print-width

## Automatic Formatting

To automatically format markdown files written by the agent:

1. Create a hook script at `~/.claude/hooks/pre-post.md-format`:

```bash
#!/bin/bash
FILE_PATH="$1"
if [[ "$FILE_PATH" == *.md ]]; then
    npx prettier --parser markdown --print-width 120 "$FILE_PATH" --write
fi
```

1. Add to your `~/.claude/settings.json`:

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

## Examples

### Before

```markdown
| Name | Age |
| ---- | --- |
| John | 25  |
| Jane | 30  |
```

### After

```markdown
| Name | Age |
| ---- | --- |
| John | 25  |
| Jane | 30  |
```

## Requirements

- Node.js and npm (required for automatic prettier installation if not present)
- Python 3.x (for the helper script)

**Note:** If Prettier is not installed, the Python script will automatically install it using `npm install -g prettier`. The bash commands require Prettier to be pre-installed or available in your PATH.

## Configuration

The skill uses Prettier's default markdown settings. You can customize by:

- Setting `print-width` for line wrapping
- Using `--prose-wrap always` for text wrapping
- Adding a `.prettierrc` file in your project for custom rules

For linting configuration, create a `.markdownlint.json` file:

```json
{
  "MD013": false,
  "default": true
}
```
