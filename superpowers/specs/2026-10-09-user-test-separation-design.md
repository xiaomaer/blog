# Separate User Validation Logic from Tests

## Goal and Scope

Separate the business code and print-based examples in `python_backend_scaffold/src/python_backend_scaffold/test.py`, preserving the behavior and type annotations of `User` and `check_user()`.

## Files and Responsibilities

- `python_backend_scaffold/src/python_backend_scaffold/user.py`: retain the `User` model and `check_user()` without test data, print statements, or a test entry point.
- `python_backend_scaffold/tests/test_user.py`: import and verify the business code with pytest.
- Remove the original `src/python_backend_scaffold/test.py`; no other references to that module were found in the repository.

Keep the model and function in the same business module without adding architectural layers. Use the project's existing pytest and Ruff dependencies; the separation requires no dependency changes.

As confirmed by the user, set `pythonpath = ["src"]` under `[tool.pytest.ini_options]` in `pyproject.toml` so pytest can import the source package without a command-line path override.

## Expected Behavior

- Active administrators return `(name, "ACTIVE")`.
- Active regular users return a `User` instance with unchanged fields.
- Inactive users raise `ValueError("User is not active")`, including administrators.
- Omitting any required field raises a Pydantic `ValidationError`.

## Validation and Delivery

Run assertion-based tests against the original module, then move the business code and update the test import. Use the same tests to verify consistent behavior before and after the refactor. Run Ruff lint and formatting checks, and manually inspect the scope of the changes.

Preserve existing workspace changes. The documents were initially written in Chinese and translated into English before the user-authorized commit, as required by the repository instructions.
