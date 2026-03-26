# QA Skeleton — Claude Code Instructions

## Project Overview

This is an automated frontend testing framework for crypto protocol interfaces using Playwright and Pytest. Tests are generated from human-authored specs.

## Directory Structure

- `specs/` — Test specifications (1:1 mapping with test files)
- `domain/protocols/` — How the crypto protocol works
- `domain/app/` — Shared UI assumptions across the application
- `skills/` — Technical recipes for reusable patterns
- `tests/` — All test code lives here:
  - `tests/conftest.py` — Shared Pytest fixtures
  - `tests/pages/` — Page objects (selectors + UI actions)
  - `tests/test_*.py` — Test files (generated from specs)

## Test Generation Workflow

When asked to implement a test:

1. Read the spec file in `specs/`
2. Read all domain docs listed in the spec's Domain References section
3. Check `skills/` for relevant technical patterns
4. Check `.env.example` for available environment variables — use these in fixtures and tests instead of hardcoding values
5. Review existing page objects in `tests/pages/`
6. Create or update the page object if needed
7. Write the test in `tests/test_<spec-filename>.py`
8. Run the test to verify it works

## Naming Conventions

- Specs: `specs/<feature-area>/<test-name>.md`
- Tests: `tests/test_<test-name>.py` — filename matches the spec
- Pages: `tests/pages/<feature>_page.py` — one per distinct page or major component
- Domain: `domain/protocols/<name>.md`, `domain/app/<name>.md`
- Skills: `skills/<name>.md`

## Coding Conventions

- One test function per spec
- Test function names match spec filenames: `specs/feature/my-test.md` → `test_my_test`
- Use fixtures from `tests/conftest.py` — never instantiate browsers or clients directly
- Page objects are the only layer that touches selectors — tests never use raw locators
- Assertions belong in the test, not in the page object
- Page objects return state (text, visibility, counts) — they do not assert
- Use Pytest markers: `@pytest.mark.smoke` for quick sanity checks, `@pytest.mark.regression` for full suite

## When Updating Existing Tests

- Read the spec first to understand intent
- Check if the page object needs updating (selector changes go in page objects)
- Check if `domain/app/` assumptions have changed
- Update the test only if the behavior changed, not just the UI

## Rules

- Do NOT invent test cases beyond what the spec describes
- Do NOT add assertions the spec doesn't call for
- Do NOT create utility functions for one-off operations
- Do NOT put selectors in test files — they belong in page objects
- Do NOT put assertions in page objects — they belong in test files
