# QA Skeleton Framework for Frontend Testing with Claude + Playwright

## Overview

A template repository ("qa-skeleton") that teams clone per project to automate frontend testing of crypto protocol interfaces using Claude Code and Playwright. The framework provides conventions, structure, and reference material that make Claude maximally effective at generating and maintaining Playwright tests from human-authored specs.

## Goals

1. **Consistent test generation** — structured spec template produces predictable, complete tests every time
2. **Maintainable test suite** — layered architecture so UI changes propagate through one or two files, not everything
3. **Fast onboarding** — new team members write a spec and get a working test on day one
4. **Optimized for Claude Code** — directory structure and conventions designed for Claude's context-gathering patterns

## Project Structure

```
qa-skeleton/
├── CLAUDE.md                      # Global test-writing rules for Claude
├── README.md                      # Onboarding workflow and project overview
├── skills/                        # Technical recipes for reusable patterns
│   ├── wallet-injection.md
│   └── transaction-polling.md
├── domain/
│   ├── protocols/                 # How the crypto protocol works (filled per project)
│   │   └── .gitkeep
│   └── app/                       # Shared UI assumptions (filled per project)
│       └── .gitkeep
├── specs/
│   ├── _template.md               # Canonical spec template
│   └── example/                   # Example spec showing template in use
│       └── successfully-request-c2flr.md
├── pages/
│   ├── __init__.py
│   └── base_page.py               # Base page object with common helpers
├── tests/
│   └── __init__.py
├── chain/                         # Optional: blockchain interaction layer
│   ├── __init__.py
│   └── client.py
├── conftest.py                    # Common Pytest fixtures
├── pyproject.toml
├── .env.example
└── .devcontainer/
    ├── devcontainer.json
    └── Dockerfile
```

### Naming Conventions

- **Specs:** `specs/<feature-area>/<test-name>.md` (e.g., `specs/faucet/request-c2flr.md`)
- **Tests:** `tests/test_<test-name>.py` — 1:1 match with spec filename
- **Pages:** `pages/<feature>_page.py` — one page object per distinct page or major component
- **Domain:** `domain/protocols/<protocol-name>.md`, `domain/app/<pattern-name>.md`
- **Skills:** `skills/<pattern-name>.md`

The 1:1 naming between specs and tests is critical — Claude can always find the spec for a test and vice versa without ambiguity.

## CLAUDE.md — The Rules Engine

CLAUDE.md teaches Claude how to work in the repo. It covers:

### Test Generation Workflow

When asked to implement a test, Claude must:

1. Read the spec file
2. Read all domain docs listed in the spec's Domain References section
3. Check `skills/` for relevant technical patterns
4. Review existing page objects in `pages/`
5. Create or update the page object if needed
6. Write the test in `tests/test_<spec-filename>.py`
7. Run the test to verify it works

### Conventions

- One test function per spec
- Test function names match spec filenames: `specs/faucet/request-c2flr.md` → `test_request_c2flr`
- Use fixtures from `conftest.py` — never instantiate browsers or clients directly
- Page objects are the only layer that touches selectors — tests never use raw locators
- Assertions belong in the test, not in the page object (page objects return state, tests assert on it)
- Use Pytest markers: `@pytest.mark.smoke` or `@pytest.mark.regression`

### When Updating Existing Tests

- Read the spec first to understand intent
- Check if the page object needs updating (selector changes go here)
- Check if domain/app assumptions have changed
- Update the test only if the behavior changed, not just the UI

### What Claude Should NOT Do

- Don't invent test cases beyond what the spec describes
- Don't add assertions the spec doesn't call for
- Don't create utility functions for one-off operations

## Spec Template

```markdown
# <Test Name>

## Context
<!-- Why does this test exist? Link to the feature/requirement it validates. -->

## Preconditions
<!-- What must be true before the test starts?
     e.g., wallet connected, specific network selected, token balance > 0 -->

## Steps
<!-- Numbered list of user actions. Each step = one interaction. -->
1. Navigate to [page]
2. Enter [value] in [field]
3. Click [button]

## Expected Results
<!-- What should happen after the steps complete?
     Be specific: UI feedback, state changes, on-chain effects. -->
- [ ] UI shows success message
- [ ] State change is verified

## Edge Cases
<!-- Known failure modes this test should NOT cover.
     Helps Claude stay scoped. Helps QA plan adjacent specs. -->

## Domain References
<!-- Which domain docs provide context for this test? -->
- Protocol: `domain/protocols/<name>.md`
- App: `domain/app/<name>.md`
```

### Template Design Decisions

- **Steps are user actions, not implementation details** — "Click the request button" not "Click `button[data-testid='request']`." Selectors belong in page objects, not specs.
- **Expected Results use checkboxes** — Claude maps each one to an assertion. Reviewers can check them off during manual verification.
- **Edge Cases section is exclusionary** — lists what this test does NOT cover, preventing Claude from over-generating and helping QA identify gaps for future specs.
- **Domain References are explicit** — Claude knows exactly which docs to read.

## Domain Knowledge Layer

### Protocol Docs (`domain/protocols/`)

Describe how the underlying crypto protocol works, independent of any UI. Written once per project, referenced by many specs.

Example:

```markdown
# Flare Faucet Protocol

## Overview
The faucet dispenses testnet C2FLR tokens on the Coston2 network.

## Mechanics
- Sends a fixed amount of C2FLR to a provided EVM address
- Rate limited: one request per address per 24 hours
- Tokens are delivered via on-chain transaction (not instant)
- Typical confirmation time: 10-30 seconds

## Key Concepts
- **C2FLR**: Testnet token on Coston2 (not real value)
- **Coston2**: Flare's test network (chain ID 114)
```

### App Docs (`domain/app/`)

Describe shared UI behaviors that are true across the application. These change when the app is redesigned, not when the protocol changes.

Example:

```markdown
# Notifications

All transaction feedback follows this pattern:
- Success: green toast with message, auto-dismisses after 5s
- Error: red toast with message, persists until dismissed
- Pending: spinner replaces the submit button until resolved

# Token Display

- Amounts are always displayed in ether (not wei)
- Balances update on a 30s polling interval, not real-time
```

### Why the Split Matters

- Protocol docs stay stable and reusable — protocol upgrades are rare
- App docs are the ones that get updated when the UI is redesigned
- Claude gets the right level of detail for each concern
- Domain docs describe what IS, not what to test — they're reference material, not specs

## Skills

Technical recipes in `./skills/` for patterns that come up across projects. They teach Claude how to handle specific technical challenges that aren't obvious from the code alone.

### What Makes a Good Skill

- **Skill:** Technical how-to that applies across multiple projects (wallet injection, transaction polling, RPC mocking)
- **Page object:** Project-specific UI interaction (not a skill)
- **Domain doc:** What the protocol/app does (not a skill)
- **CLAUDE.md:** Rules and conventions (not a skill)

### Skill Format

```markdown
# <Pattern Name>

## When to Use
<!-- What situation triggers this pattern? -->

## Approach
<!-- High-level strategy -->

## Implementation Pattern
<!-- Step-by-step technical recipe -->

## Gotchas
<!-- Common mistakes and edge cases -->
```

Skills ship with the skeleton if they're broadly applicable. Project teams add project-specific skills as needed.

## Test Architecture & Layering

Each layer has one job and a clear boundary:

```
specs/          → WHAT to test (human-authored)
    ↓
domain/         → WHY it works this way (protocol + app context)
    ↓
skills/         → HOW to handle technical patterns (reference material)
    ↓
pages/          → WHERE to interact (selectors + UI actions)
    ↓
tests/          → GLUE — reads spec intent, uses page objects, asserts results
    ↓
conftest.py     → INFRASTRUCTURE — fixtures, browser config, env setup
```

### Change Propagation Matrix

| UI Change | What to Update |
|---|---|
| Selector changes (button renamed, new data-testid) | `pages/` only |
| UX flow changes (new step, modal replaced by inline) | `pages/` + `specs/` |
| Protocol change (new rate limit, different token amount) | `domain/protocols/` + affected `specs/` |
| App-wide pattern change (toast redesign, new nav) | `domain/app/` + affected `pages/` |
| New test case | Add a `spec`, Claude generates `pages/` updates + `test` |

### Layer Rules

- Tests never import from page object internals — only use public methods
- Page objects never assert — they return state (text, visibility, counts)
- Tests never use raw selectors — `page.locator()` in a test file is wrong
- One page object per distinct page or major component
- Fixtures own setup/teardown — tests read like the spec steps

## Audience & Workflow

### Who Writes What

- **QA engineers** are the primary spec authors
- **Anyone on the team** can write a spec if they follow the template
- **Claude** generates tests, page objects, and updates from specs
- **Domain experts** write protocol and app docs

### Adding a Test

1. Write a spec using `specs/_template.md`
2. Ask Claude to implement the test from the spec
3. Claude reads spec → domain refs → skills → page objects → writes the test
4. Run the test, iterate

### When a Test Breaks

1. Identify which layer changed (use the Change Propagation Matrix)
2. Update that layer
3. Claude can help if pointed at the failing test + updated spec

### Starting a New Project

1. Clone the skeleton repo
2. Fill in `domain/protocols/` with the protocol description
3. Fill in `domain/app/` with shared UI assumptions
4. Write specs using the template
5. Ask Claude to generate tests from specs
