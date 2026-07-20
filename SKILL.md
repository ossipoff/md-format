---
name: md-format
description: |
  Formats markdown content using Prettier to ensure proper structure, readable tables, correct line breaks, and consistent styling. Automatically checks for and installs Prettier if needed. Use this skill whenever AI-generated markdown needs formatting, when you see poorly formatted tables or missing line breaks in markdown, or when you want to clean up markdown output from AI agents. This skill handles both raw text strings and file paths.
compatibility: claude-code opencode
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# md-format: Markdown Formatter

This skill formats markdown content using Prettier to fix common issues like:

- Unreadable or misaligned tables
- Missing line breaks between elements
- Inconsistent heading spacing
- Poor list formatting
- Code block issues

## Enhanced Features

The skill now includes:

- **Linting integration** with markdownlint-cli
- **Markdownlint auto-fix** for issues like MD026, MD029, etc.
- **Technical mode** for documents with equations/code (relaxed line-length rules)
- **Auto-fix mode** for CI/CD pipelines
- **Configuration support** via `.markdownlint.json` and `.prettierrc` files

## When to use this skill

Use this skill when:

- AI generates markdown with broken tables
- You see missing blank lines in markdown output
- Markdown looks "squished" or hard to read
- You want to ensure consistent markdown formatting

## How it works

The skill uses `prettier --parser markdown` to format markdown content. Prettier handles tables much better than basic markdown linters because it understands the semantic structure of markdown elements.

## Usage Patterns

### Pattern 1: Format markdown text directly

When you have markdown as a string that needs formatting:

```markdown
| Input: | Header1 | Header2 |
| ------ | ------- | ------- |
| Cell1  | Cell2   |

| Output: | Header1 | Header2 |
| ------- | ------- | ------- |
| Cell1   | Cell2   |
```

### Pattern 2: Format a markdown file

When you have a `.md` file that needs formatting:

```bash
prettier --write path/to/file.md
```

### Pattern 3: Format and return as string

When you need formatted markdown returned as a string for immediate use.

## Workflow

1. **Identify the input** - Determine if you have raw markdown text or a file path
2. **Choose the method** - Use the appropriate approach based on input type
3. **Format with Prettier** - Run prettier with markdown parser
4. **Return or save** - Return formatted string or write to file

## Examples

### Example 1: Fix broken table alignment

**Before:**

```markdown
| Name | Age | City |
|John|25|NYC|
|Jane|30|LA|
```

**After:**

```markdown
| Name | Age | City |
| ---- | --- | ---- |
| John | 25  | NYC  |
| Jane | 30  | LA   |
```

### Example 2: Add missing line breaks

**Before:**

```markdown
# Heading## Subheading

- Item 1
- Item 2
```

**After:**

```markdown
# Heading

## Subheading

- Item 1
- Item 2
```

## Implementation

### Step 1: Check for Prettier

Before formatting, the skill checks if Prettier is available:

```bash
# Check if prettier is installed
if ! command -v prettier &> /dev/null; then
    echo "Prettier not found. Installing..."
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

# Format and save to output
prettier --parser markdown path/to/input.md > path/to/output.md
```

### Key Options Used

- `--parser markdown` - Parse as markdown
- `--prose-wrap always` - Wrap prose for readability (optional)
- `--print-width 80` - Standard line length (can be adjusted)

### Step 3: Handle Missing Dependencies

If Prettier is not installed, the skill will:

1. Check for `npm` availability
2. Install Prettier globally using `npm install -g prettier`
3. Retry the formatting operation

**Note:** If you don't have Node.js/npm installed, you'll need to install it first. The skill cannot bypass this requirement.

## Enhanced Workflow with Linting

### Technical Mode

For technical documents with equations, code snippets, and long lines:

```bash
# Use technical mode for relaxed line length (120 chars)
python scripts/format_and_lint.py --technical path/to/file.md

# Auto-fix all issues
python scripts/format_and_lint.py --fix --technical path/to/file.md
```

### CI/CD Integration

For continuous integration pipelines:

```bash
# Exit with error code on any issue
python scripts/format_and_lint.py --ci path/to/file.md

# Only check specific files
python scripts/format_and_lint.py --ci file1.md file2.md
```

### Fixing Issues

The `--fix` option runs both Prettier formatting AND markdownlint fixes in sequence:

```bash
# Fix everything: Prettier formatting + markdownlint issues
python scripts/format_and_lint.py --fix path/to/file.md
```

This handles:

- Table alignment and spacing (Prettier)
- Trailing punctuation in headings (markdownlint MD026)
- Ordered list numbering (markdownlint MD029)
- Other auto-fixable markdownlint rules

Some markdownlint rules require manual intervention and cannot be auto-fixed.

### Configuration Files

Create `.markdownlint.json` in your project root:

```json
{
  "MD013": false,
  "MD033": false,
  "default": true
}
```

Create `.prettierrc` for custom formatting rules:

```json
{
  "printWidth": 120,
  "proseWrap": "always"
}
```

### Common Issues Fixed

| Issue                        | How It's Fixed                           |
| ---------------------------- | ---------------------------------------- |
| Long lines in technical docs | Technical mode uses 120 char line length |
| Broken tables                | Prettier aligns columns automatically    |
| Missing blank lines          | Prettier adds proper spacing             |
| Trailing whitespace          | Removed during formatting                |

## Automatic Formatting Setup

To automatically format markdown files written by the agent, you can set up a Claude Code hook:

### Option 1: Post-write Hook (Manual Setup)

Create a hook script at `~/.claude/hooks/pre-post.md-format`:

```bash
#!/bin/bash
FILE_PATH="$1"
if [[ "$FILE_PATH" == *.md ]]; then
    npx prettier --parser markdown --print-width 120 "$FILE_PATH" --write
fi
```

Then add to your `~/.claude/settings.json`:

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

### Option 2: Use the Skill Directly

For immediate formatting after writing markdown:

```bash
# Format a file
/md-format path/to/file.md

# Format with technical mode for code/equations
python scripts/format_and_lint.py --technical --fix path/to/file.md
```

### Option 3: CI/CD Integration

For automated checks in pipelines:

```bash
# Check if markdown passes linting
python scripts/format_and_lint.py --ci path/to/file.md

# Exit code 1 if issues found, 0 if clean
```

## Triggering the Skill

The skill can be triggered in multiple ways:

1. **Direct invocation**: `/md-format` or `/md-format <file-path>`
2. **Python script**: `python scripts/format_and_lint.py <options> <files>`
3. **Prettier CLI**: `npx prettier --parser markdown <file>`

For automatic triggering on all markdown writes, set up the hook configuration above.
