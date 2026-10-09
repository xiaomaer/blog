# User Validation Test Separation Plan

Related design: `../specs/2026-10-09-user-test-separation-design.md`.

## 1. Establish a Behavior Baseline

- Import `User` and `check_user()` from the original module in `python_backend_scaffold/tests/test_user.py`.
- Convert the administrator, regular-user, and missing-field examples into assertions, and add inactive-user cases.
- Validate from `python_backend_scaffold/` with `poetry run python -B -m pytest -p no:cacheprovider -o pythonpath=src`.

## 2. Separate the Business Module

- Move the model and function to `src/python_backend_scaffold/user.py`.
- Remove the print-based examples, test-only import, and original `test.py`.
- Update the test import to `python_backend_scaffold.user`.
- Run the same pytest command again and verify consistent results.
- As confirmed by the user, add `[tool.pytest.ini_options]` with `pythonpath = ["src"]` to `pyproject.toml`, then run `poetry run python -B -m pytest -p no:cacheprovider` without the temporary path override.

## 3. Verify Delivery

- Run `poetry run ruff check --no-cache src/python_backend_scaffold/user.py tests/test_user.py`.
- Run `poetry run ruff format --check --no-cache src/python_backend_scaffold/user.py tests/test_user.py`.
- Manually confirm that the business module has no test entry point, return values and exception rules are unchanged, and existing workspace changes are preserved.
- Report the actual commands, exit codes, file responsibilities, and commit status.

## Execution Record

- The first pytest run without a source path failed during collection with exit code `2`: the project package was not installed in the current Poetry environment, so modules under `src/` could not be imported.
- With the command-line override `-o pythonpath=src`, both the baseline and post-refactor runs reported `7 passed` with exit code `0`.
- Ruff lint reported `All checks passed!` with exit code `0`.
- Ruff formatting checks reported `2 files already formatted` with exit code `0`.
- Manual inspection confirmed that the business module contains only the model and function, with unchanged return values, validation order, and exception messages.
- The user selected project-level pytest path configuration; `pythonpath = ["src"]` was added to `pyproject.toml` without adding dependencies.
- After configuring the path, `poetry run python -B -m pytest -p no:cacheprovider` reported `7 passed in 0.12s` with exit code `0`, without a temporary source path override.
