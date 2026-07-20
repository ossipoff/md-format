#!/usr/bin/env python3
"""
Markdown formatter and linter wrapper for Prettier + markdownlint-cli.

This script provides comprehensive markdown processing including:
- Formatting with Prettier
- Linting with markdownlint-cli
- Technical document support (relaxed line-length rules)
- Configuration file support

Usage:
    # Format and lint from stdin
    echo "# Heading" | python format_and_lint.py

    # Format and lint a file
    python format_and_lint.py path/to/file.md

    # Format and lint with technical mode (relaxed line length)
    python format_and_lint.py --technical path/to/file.md

    # Auto-fix issues
    python format_and_lint.py --fix path/to/file.md

    # Show only errors (CI-friendly)
    python format_and_lint.py --ci path/to/file.md
"""

import subprocess
import sys
import shutil
from pathlib import Path
import json
import fnmatch


# Constants
DEFAULT_PRINT_WIDTH = 80
TECHNICAL_PRINT_WIDTH = 120


def check_tool_installed(tool_name: str) -> bool:
    """Check if a tool is installed and available."""
    return shutil.which(tool_name) is not None


def install_npm_package(package: str) -> bool:
    """Install an npm package globally."""
    print(f"Installing {package}...", file=sys.stderr)

    if not shutil.which("npm"):
        print("Error: npm is not installed. Please install Node.js first.", file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            ["npm", "install", "-g", package],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{package} installed successfully.", file=sys.stderr)
            return True
        else:
            print(f"Error installing {package}: {result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Error during {package} installation: {e}", file=sys.stderr)
        return False


def ensure_tools(need_prettier: bool = True, need_lint: bool = True) -> bool:
    """Ensure required tools are installed."""
    success = True

    # For prettier, try global installation first, then npx fallback
    if need_prettier:
        if not check_tool_installed("prettier"):
            print("Prettier not found. Installing prettier globally...", file=sys.stderr)
            if not install_npm_package("prettier"):
                print("Warning: Will fall back to npx for Prettier", file=sys.stderr)

    # Install markdownlint-cli globally as well
    if need_lint:
        if not check_tool_installed("markdownlint"):
            print("markdownlint not found. Installing markdownlint-cli globally...", file=sys.stderr)
            if not install_npm_package("markdownlint-cli"):
                print("Warning: Will fall back to npx for markdownlint", file=sys.stderr)

    return success


def should_ignore_file(file_path: str) -> bool:
    """
    Check if a file should be ignored based on .md-format-ignore file.

    Looks for .md-format-ignore in the file's directory and parent directories.
    Returns True if the file matches any pattern in the ignore file.
    """
    path = Path(file_path).resolve()  # Use absolute path to handle relative paths correctly
    filename = path.name

    # Look for .md-format-ignore file starting from the file's directory
    current_dir = path.parent
    while current_dir != current_dir.parent:  # Stop at root
        ignore_file = current_dir / ".md-format-ignore"
        if ignore_file.exists():
            try:
                with open(ignore_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if not line or line.startswith('#'):
                            continue

                        # Check if filename matches the pattern
                        # Support glob-style patterns
                        if fnmatch.fnmatch(filename, line) or fnmatch.fnmatch(str(path), '*' + line):
                            return True
            except Exception as e:
                print(f"Warning: Could not read {ignore_file}: {e}", file=sys.stderr)
            break

        current_dir = current_dir.parent

    return False


def format_markdown(text: str, technical_mode: bool = False, print_width: int = None) -> str:
    """Format markdown text using Prettier."""
    # Try direct prettier command first, fall back to npx
    args = ["prettier", "--parser", "markdown"]

    # Set print width based on mode or explicit value
    if print_width:
        args.extend(["--print-width", str(print_width)])
    elif technical_mode:
        # In technical mode, allow longer lines for equations and code
        args.extend(["--print-width", str(TECHNICAL_PRINT_WIDTH)])

    result = subprocess.run(
        args,
        input=text,
        capture_output=True,
        text=True
    )

    # Fall back to npx if prettier not found
    if result.returncode != 0 and "command not found" in result.stderr.lower():
        args = ["npx", "prettier", "--parser", "markdown"]
        if print_width:
            args.extend(["--print-width", str(print_width)])
        elif technical_mode:
            args.extend(["--print-width", str(TECHNICAL_PRINT_WIDTH)])
        result = subprocess.run(
            args,
            input=text,
            capture_output=True,
            text=True
        )

    if result.returncode != 0:
        print(f"Error formatting markdown: {result.stderr}", file=sys.stderr)
        return text

    return result.stdout


def lint_markdown(file_path: str, technical_mode: bool = False) -> tuple[bool, list[str]]:
    """
    Lint markdown file using markdownlint-cli.
    Returns (has_errors, error_list).
    """
    # Try direct command first, fall back to npx
    args = ["markdownlint", str(file_path)]

    # In technical mode, use relaxed rules
    config_path = None
    if technical_mode:
        # Create a temporary config with relaxed line length
        config = {
            "MD013": False,  # Disable line length rule
            "MD033": False,  # Allow inline HTML
        }
        config_path = Path(file_path).parent / ".markdownlint-tmp.json"
        config_path.write_text(json.dumps(config))
        args.extend(["--config", str(config_path)])

    result = subprocess.run(
        args,
        capture_output=True,
        text=True
    )

    # Fall back to npx if markdownlint not found
    if result.returncode != 0 and ("command not found" in result.stderr.lower() or result.returncode == 127):
        args = ["npx", "markdownlint-cli", str(file_path)]
        if technical_mode:
            args.extend(["--config", str(config_path)])
        result = subprocess.run(
            args,
            capture_output=True,
            text=True
        )

    errors = []
    if result.returncode != 0:
        # Combine both streams — some tools write to one or the other depending on platform/version
        for line in (result.stdout + "\n" + result.stderr).strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("✔") and "markdownlint" not in line.lower():
                errors.append(line)

    # Clean up temp config
    if config_path and config_path.exists():
        config_path.unlink()

    return result.returncode == 0, errors


def fix_markdownlint(file_path: str, technical_mode: bool = False) -> tuple[bool, list[str]]:
    """
    Fix markdown issues using markdownlint-cli --fix.
    Returns (success, error_list).
    """
    # Try direct command first, fall back to npx
    args = ["markdownlint", "--fix", str(file_path)]

    # In technical mode, use relaxed rules
    config_path = None
    if technical_mode:
        config = {
            "MD013": False,  # Disable line length rule
            "MD033": False,  # Allow inline HTML
        }
        config_path = Path(file_path).parent / ".markdownlint-tmp.json"
        config_path.write_text(json.dumps(config))
        args.extend(["--config", str(config_path)])

    result = subprocess.run(
        args,
        capture_output=True,
        text=True
    )

    # Fall back to npx if markdownlint not found
    if result.returncode != 0 and ("command not found" in result.stderr.lower() or result.returncode == 127):
        args = ["npx", "markdownlint-cli", "--fix", str(file_path)]
        if technical_mode:
            args.extend(["--config", str(config_path)])
        result = subprocess.run(
            args,
            capture_output=True,
            text=True
        )

    errors = []
    if result.returncode != 0:
        # Combine both streams — some tools write to one or the other depending on platform/version
        for line in (result.stdout + "\n" + result.stderr).strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("✔") and "markdownlint" not in line.lower():
                errors.append(line)

    # Clean up temp config
    if config_path and config_path.exists():
        config_path.unlink()

    return result.returncode == 0, errors


def format_file(file_path: str, write: bool = False, technical_mode: bool = False, print_width: int = None) -> str:
    """Format a markdown file using Prettier."""
    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        return ""

    content = path.read_text()
    formatted = format_markdown(content, technical_mode=technical_mode, print_width=print_width)

    if write:
        path.write_text(formatted)
        print(f"Formatted: {file_path}")

    return formatted


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Format and lint markdown files with Prettier and markdownlint-cli. "
                    "By default, checks only without modifying files."
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument("--output", "-o", help="Output file (for stdin input)")
    parser.add_argument("--write", "-w", action="store_true", default=False,
                        help="Write changes to file (default: check only)")
    parser.add_argument("--fix", "-f", action="store_true", default=False,
                        help="Fix both Prettier formatting and markdownlint issues (implies --write)")
    parser.add_argument("--dry-run", "-d", action="store_true",
                        help="Show what would change without modifying files")
    parser.add_argument("--print-width", type=int, default=None,
                        help="Line length for wrapping (default: 80, or 120 in technical mode)")
    parser.add_argument("--technical", "-t", action="store_true",
                        help="Technical mode - relaxed line length rules for code/equations")
    parser.add_argument("--check", "-c", action="store_true",
                        help="Check only - don't modify files")
    parser.add_argument("--ci", action="store_true",
                        help="CI mode - exit with error code on any issue")
    parser.add_argument("--no-lint", action="store_true",
                        help="Skip linting step")
    parser.add_argument("--no-format", action="store_true",
                        help="Skip formatting step")

    args = parser.parse_args()

    # If --check is set, disable write mode
    if args.check:
        args.write = False

    # --fix implies --write (and includes markdownlint fixes)
    if args.fix:
        args.write = True

    # Ensure tools are available
    if not ensure_tools(need_lint=not args.no_lint):
        print("Warning: Some tools could not be installed.", file=sys.stderr)

    has_issues = False

    if args.files:
        # Process files
        for file_path in args.files:
            path = Path(file_path)

            if not path.exists():
                print(f"File not found: {file_path}", file=sys.stderr)
                has_issues = True
                continue

            # Check if file should be ignored
            if should_ignore_file(file_path):
                print(f"Skipping ignored file: {file_path}", file=sys.stderr)
                continue

            content = path.read_text()

            # Format
            if not args.no_format:
                formatted = format_markdown(content, technical_mode=args.technical, print_width=args.print_width)
                if formatted != content:
                    if args.dry_run:
                        print(f"\n--- Changes for {file_path} ---")
                        print("Original:")
                        print(content[:500] + "..." if len(content) > 500 else content)
                        print("\nFormatted:")
                        print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
                    elif args.write or args.fix:
                        path.write_text(formatted)
                        print(f"Formatted: {file_path}")
                    else:
                        print(f"Formatting changes needed for: {file_path}")

            # Lint
            if not args.no_lint:
                is_clean, errors = lint_markdown(file_path, technical_mode=args.technical)
                if not is_clean:
                    has_issues = True
                    # In --fix mode, defer printing until after the fix attempt so we don't show
                    # duplicates of what got resolved vs what couldn't be auto-fixed.
                    if not args.fix:
                        for error in errors[:10]:  # Show first 10 errors
                            print(f"  {error}")
                        if len(errors) > 10:
                            print(f"  ... and {len(errors) - 10} more errors")

            # Fix markdownlint issues if --fix is enabled (runs after Prettier formatting)
            if args.fix and not args.no_lint:
                success, fix_errors = fix_markdownlint(file_path, technical_mode=args.technical)
                if not success:
                    for err in fix_errors[:5]:
                        print(f"  Unresolved: {err}", file=sys.stderr)
                    if len(fix_errors) > 5:
                        print(f"  ... and {len(fix_errors) - 5} more unresolved", file=sys.stderr)

    else:
        # Read from stdin
        text = sys.stdin.read()

        # Format
        if not args.no_format:
            formatted = format_markdown(text, technical_mode=args.technical, print_width=args.print_width)
        else:
            formatted = text

        if args.dry_run and formatted != text:
            print("--- Dry run - changes that would be made ---")
            print("Original:")
            print(text[:500] + "..." if len(text) > 500 else text)
            print("\nFormatted:")
            print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
        elif args.output:
            Path(args.output).write_text(formatted)
            print(f"Written to {args.output}")
        else:
            print(formatted)

    if args.ci and has_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()