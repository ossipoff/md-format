# md-format Skill

A simple tool to fix messy markdown files automatically.

## Why Use This?

When AI generates markdown or you write documentation, the output often has issues:

- Tables that don't align properly
- Missing blank lines between sections
- Inconsistent spacing around headings
- Lists that look squished together

This skill fixes all of these problems automatically using Prettier, the same tool used by professional developers worldwide.

## Quick Installation

### Option 1: Install as a Claude Code Skill (Recommended)

1. Copy this repository to your machine:

   ```bash
   git clone https://github.com/ossipoff/md-format.git
   cd md-format
   ```

2. The skill is now ready to use! You can invoke it directly in Claude Code with `/md-format`.

### Option 2: Use the Python Script Directly

If you just want to format markdown files without installing as a skill:

```bash
# Format a file (check mode - shows what needs fixing)
python scripts/format_and_lint.py path/to/file.md

# Auto-fix and save changes
python scripts/format_and_lint.py --fix path/to/file.md
```

## What It Does

The skill automatically fixes common markdown problems:

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

It also adds missing blank lines, aligns tables, and ensures consistent spacing throughout your document.

## How It Helps You

- **Saves time**: No more manual formatting of tables and lists
- **Improves readability**: Clean, professional-looking documentation
- **Reduces errors**: Consistent formatting prevents mistakes
- **Works automatically**: Set up once, forget about it

## Automatic Formatting Setup

Want markdown files to be formatted automatically every time you write them? Here's how:

1. Create a hook script at `~/.claude/hooks/pre-post.md-format`:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.filePath // .path // empty' 2>/dev/null | grep -E '\.md$' | head -1)
if [ -n "$FILE_PATH" ] && [[ "$FILE_PATH" == *.md ]]; then
    python /path/to/md-format/scripts/format_and_lint.py --fix "$FILE_PATH" 2>/dev/null || true
fi
exit 0
```

2. Add this to your `~/.claude/settings.json`:

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

Now every time you write a `.md` file, it will be automatically formatted!

## Examples

### Fix Broken Tables

**Before:**

```markdown
|Product|Price|Stock|
|-------|-----|-----|
|Widget| $5 | 100 |
|Gadget|$10| 50 |
```

**After:**

```markdown
| Product | Price | Stock |
| ------- | ----- | ----- |
| Widget  | $5    | 100   |
| Gadget  | $10   | 50    |
```

### Add Missing Line Breaks

**Before:**

```markdown
# Title## Subtitle

- Item 1
- Item 2
```

**After:**

```markdown
# Title

## Subtitle

- Item 1
- Item 2
```

## Requirements

- Node.js and npm (the script will auto-install Prettier if needed)
- Python 3.x

## Configuration

### Ignore Files

By default, the skill will format all markdown files. If you want to skip certain files (like README.md or SKILL.md), create a `.md-format-ignore` file in your project:

```bash
# .md-format-ignore
README.md
SKILL.md
*.generated.md
```

One pattern per line. Lines starting with `#` are comments. The skill checks for this file automatically when formatting.

### Linting with markdownlint-cli

The skill also checks your markdown for common issues using markdownlint-cli. This catches problems like:

- Trailing punctuation in headings (MD026)
- Inconsistent list numbering (MD029)
- Line length violations (MD013)
- And many other style issues

To fix linting issues automatically, use the `--fix` flag:

```bash
python scripts/format_and_lint.py --fix path/to/file.md
```

This runs both Prettier formatting AND markdownlint fixes in one command.

### Customize Formatting

The skill uses sensible defaults, but you can customize:

- Create `.prettierrc` for custom formatting rules
- Use `--technical` flag for documents with code/equations (120 char lines)
- Use `--print-width 100` to set custom line length

## Getting Help

Run the skill directly in Claude Code with `/md-format` or check the [SKILL.md](SKILL.md) file for detailed documentation.
