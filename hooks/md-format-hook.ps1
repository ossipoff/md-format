# PostToolUse hook: format markdown after Write/Edit.
#
# Replaces the md-format skill's bash hook (hooks/md-format-hook.sh), which
# needs jq and a POSIX shell. This reads the hook payload from stdin, and exits
# quietly for anything that is not an existing .md file.

$ErrorActionPreference = 'Continue'

$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try { $payload = $raw | ConvertFrom-Json } catch { exit 0 }

$file = $payload.tool_input.file_path
if (-not $file) { $file = $payload.tool_response.filePath }
if (-not $file -or $file -notmatch '\.md$') { exit 0 }
if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { exit 0 }

# This file lives in <skill-root>\hooks\, so the script is one level up.
$script = Join-Path $PSScriptRoot '..\scripts\format_and_lint.py'
if (-not (Test-Path -LiteralPath $script -PathType Leaf)) { exit 0 }

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { exit 0 }

# UTF-8 so Danish characters survive the round trip through the formatter.
$env:PYTHONUTF8 = '1'

# --technical relaxes MD013/MD033, which every markdown table trips over.
& $python $script --fix --technical $file 2>&1 | Out-Null

exit 0
