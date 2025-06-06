---
applyTo: '**'
---

# Python 3.10+ Package Instructions

## Tools and Libraries
- Support Python 3.10 and above.
- Use `pip` for package management.
- Use `pyproject.toml` for project configuration.
- Use `mypy` for static type checking.
- Use `flake8` and `pylint` for code linting.
- Use `isort` for sorting imports.
- Use `pytest` for testing.

## Code Style
- Follow PEP 8 for style guidelines.
- Try to create a code which follows `flake8` and `pylint` standards.
- Indent with 4 spaces.
- Do not use obsolete features.
- Use all modern recommendations and features when suitable.

### Code Structure
- Do not combine different functionalities in a single function. Focus on single responsibility.
- Make functions testable and reusable.
- Put all source code for the package in a single directory named `src`.
- Use a `tests` directory for unit tests.

### Identifiers
- Use descriptive variable and function names.
- Do not shorten words in identifiers unless necessary and they are widely recognized abbreviations.

### Type Hints
- Use type hints where applicable - including function signatures, variables, class attributes, etc.
- Use type hints also in test code.
- Use `from __future__ import annotations` to enable postponed evaluation of type annotations.

### Docstrings
- The module docstring is at the top of the file, immediately after the shebang line (if present) separated by a single blank line.
- Create docstrings for all public modules, classes, class variables, methods, and functions.
- The first line of the docstring is a short summary starting with a capital letter and ending with a period.
- The first line starts with a verb in the imperative mood.
- Use Google style for docstrings.
