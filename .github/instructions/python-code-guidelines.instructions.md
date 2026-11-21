---
applyTo: "**/*.py"
---

# Python code guidelines

These guidelines are intentionally concise and align with recommendations from the Python documentation and commonly accepted standards such as PEP 8 and PEP 20.

## Style and formatting

- Follow PEP 8 for code style.
- Use 4 spaces per indentation level; do not use tabs.
- Keep lines reasonably short (typically 79-88 characters unless project standards differ).
- Use descriptive, meaningful names for variables, functions, classes, and modules.
- Use `snake_case` for functions, methods, variables, and modules.
- Use `PascalCase` for class names.
- Use `UPPER_CASE` for constants.

## Imports

- Place imports at the top of the file.
- Group imports as: standard library, third-party packages, then local imports.
- Prefer explicit imports over wildcard imports (`from module import *`).

## Functions and classes

- Keep functions focused on a single responsibility.
- Write docstrings for public modules, classes, and functions.
- Prefer small, composable functions over deeply nested logic.
- Use type hints when they improve readability and maintainability.

## Readability

- Prefer clear and explicit code over clever or overly compact solutions.
- Follow the principle: "Readability counts."
- Avoid unnecessary comments; write self-explanatory code and use comments only when they add context.
- Use meaningful error messages and exceptions.

## Error handling

- Catch specific exceptions instead of using bare `except:` blocks.
- Use exceptions for exceptional situations, not normal control flow.
- Clean up resources using context managers (`with` statements) when appropriate.

## General practices

- Avoid mutable default argument values.
- Write tests for non-trivial behavior.
- Keep dependencies minimal and justified.
- Prefer standard library solutions before introducing external packages.
- Ensure code is maintainable, predictable, and easy to review.

## Guiding principles

When in doubt, follow the spirit of the Zen of Python:

- Explicit is better than implicit.
- Simple is better than complex.
- Readability counts.
- There should be one obvious way to do it.

## Indentation

- Use 4 spaces per indentation level.
