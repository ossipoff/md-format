# Contributing to md-format

Thank you for your interest in contributing to md-format! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/doj/md-format.git
   cd md-format
   ```

2. Install dependencies:
   - Node.js and npm (for Prettier and markdownlint-cli)
   - Python 3.x (for the helper script)

3. The script will automatically install Prettier if not found.

## Running Tests

Run the evaluation tests:

```bash
# Run all evals
python scripts/format_and_lint.py --help

# Test specific functionality
echo "# Test" | python scripts/format_and_lint.py
```

## Code Style

- Follow existing code patterns in `scripts/format_and_lint.py`
- Use meaningful variable names
- Add docstrings to new functions
- Keep line length under 100 characters (or use technical mode for longer lines)

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run tests to ensure everything works
4. Update documentation if needed
5. Submit a pull request with a clear description of changes

## Reporting Issues

If you find a bug or have a feature request, please open an issue with:

- A clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Environment details (OS, Node.js version, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
