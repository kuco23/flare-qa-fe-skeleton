# QA Skeleton — Frontend Testing with Claude + Playwright

Automated frontend testing framework for crypto protocol interfaces. Clone this repo per project, fill in domain knowledge, write specs, and let Claude generate Playwright tests.

## Quick Start

### 1. Clone and Set Up

```bash
# Clone the skeleton
git clone <skeleton-repo-url> my-project-qa
cd my-project-qa

# Open in devcontainer (recommended) or install manually
uv sync
playwright install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your project's URLs and endpoints
```

### 3. Fill In Domain Knowledge

Describe your protocol in `domain/protocols/`:

```bash
cp domain/protocols/.gitkeep domain/protocols/my-protocol.md
# Write: what the protocol does, its mechanics, key concepts
```

Document shared UI patterns in `domain/app/`:

```bash
cp domain/app/.gitkeep domain/app/notifications.md
# Write: toast patterns, wallet UX, display conventions
```

### 4. Write a Spec

```bash
cp specs/_template.md specs/my-feature/my-test-case.md
# Fill in: Context, Preconditions, Steps, Expected Results, Domain References
```

### 5. Generate the Test

Ask Claude:

> Implement the test from `specs/my-feature/my-test-case.md`

Claude will:
1. Read the spec
2. Read referenced domain docs
3. Check `skills/` for relevant technical patterns
4. Review existing page objects in `tests/pages/`
5. Create or update page objects as needed
6. Write the test in `tests/test_my_test_case.py`

### 6. Run Tests

```bash
# Run all tests
pytest

# Run smoke tests only
pytest -m smoke

# Run with visible browser
pytest --headed
```

## Project Structure

```
├── CLAUDE.md              # Rules for how Claude writes tests
├── skills/                # Technical recipes (wallet injection, etc.)
├── domain/
│   ├── protocols/         # How the crypto protocol works
│   └── app/               # Shared UI assumptions
├── specs/
│   ├── _template.md       # Spec template — start here
│   └── <feature>/         # Specs organized by feature area
└── tests/                 # All test code lives here
    ├── conftest.py        # Shared fixtures
    ├── pages/             # Page objects (selectors + UI actions)
    └── test_*.py          # Test files (1:1 with specs)
```

## Day-to-Day Workflows

### Adding a Test

1. Write a spec using `specs/_template.md`
2. Ask Claude to implement the test from the spec
3. Run the test, iterate

### When a Test Breaks

| What Changed | What to Update |
|---|---|
| Selector renamed | `tests/pages/` only |
| UX flow changed | `tests/pages/` + `specs/` |
| Protocol changed | `domain/protocols/` + affected `specs/` |
| App-wide UI pattern changed | `domain/app/` + affected `tests/pages/` |

### Starting a New Project

1. Clone the skeleton
2. Fill in `domain/protocols/` and `domain/app/`
3. Write specs, let Claude generate tests

## Key Conventions

- **Specs describe user actions**, not selectors or implementation details
- **1:1 mapping** between spec files and test files, matched by filename
- **Page objects** (`tests/pages/`) **own all selectors** — tests never use raw locators
- **Page objects don't assert** — they return state, tests assert on it
- **Fixtures handle setup** — tests read like spec steps

Read `CLAUDE.md` for the full set of conventions.
