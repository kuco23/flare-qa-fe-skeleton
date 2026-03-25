# QA Skeleton Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the existing flare-faucet-qa repo into the qa-skeleton template framework, adding CLAUDE.md, structured spec template, domain knowledge layer, skills directory, and reorganized specs — while preserving all existing working code.

**Architecture:** Layered convention framework: CLAUDE.md (rules) → domain/ (context) → skills/ (recipes) → specs/ (test descriptions) → pages/ (selectors) → tests/ (assertions) → conftest.py (infrastructure). Existing code in pages/, tests/, chain/, and conftest.py is already well-structured and needs minimal changes.

**Tech Stack:** Python 3.11+, Pytest, Playwright, web3.py, UV package manager

---

### Task 1: Create CLAUDE.md

The rules engine that teaches Claude how to work in this repo. This is the most important file in the framework.

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write CLAUDE.md**

```markdown
# QA Skeleton — Claude Code Instructions

## Project Overview

This is an automated frontend testing framework for crypto protocol interfaces using Playwright and Pytest. Tests are generated from human-authored specs.

## Directory Structure

- `specs/` — Test specifications (1:1 mapping with test files)
- `domain/protocols/` — How the crypto protocol works
- `domain/app/` — Shared UI assumptions across the application
- `skills/` — Technical recipes for reusable patterns
- `pages/` — Page objects (selectors + UI actions)
- `tests/` — Test files (generated from specs)
- `chain/` — Blockchain interaction layer (optional, project-specific)
- `conftest.py` — Shared Pytest fixtures

## Test Generation Workflow

When asked to implement a test:

1. Read the spec file in `specs/`
2. Read all domain docs listed in the spec's Domain References section
3. Check `skills/` for relevant technical patterns
4. Review existing page objects in `pages/`
5. Create or update the page object if needed
6. Write the test in `tests/test_<spec-filename>.py`
7. Run the test to verify it works

## Naming Conventions

- Specs: `specs/<feature-area>/<test-name>.md`
- Tests: `tests/test_<test-name>.py` — filename matches the spec
- Pages: `pages/<feature>_page.py` — one per distinct page or major component
- Domain: `domain/protocols/<name>.md`, `domain/app/<name>.md`
- Skills: `skills/<name>.md`

## Coding Conventions

- One test function per spec
- Test function names match spec filenames: `specs/faucet/request-c2flr.md` → `test_request_c2flr`
- Use fixtures from `conftest.py` — never instantiate browsers or clients directly
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
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Add CLAUDE.md with test generation conventions"
```

---

### Task 2: Create directory structure for domain knowledge and skills

Set up the empty directory structure that each project fills in.

**Files:**
- Create: `domain/protocols/.gitkeep`
- Create: `domain/app/.gitkeep`
- Create: `skills/.gitkeep`

- [ ] **Step 1: Create directories with .gitkeep files**

```bash
mkdir -p domain/protocols domain/app skills
touch domain/protocols/.gitkeep domain/app/.gitkeep skills/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add domain/ skills/
git commit -m "Add domain knowledge and skills directory structure"
```

---

### Task 3: Create the spec template

The canonical spec template that all team members use to write test specifications.

**Files:**
- Create: `specs/_template.md`
- Delete: `specs/fe-qa-template.md` (replaced by `_template.md`)

- [ ] **Step 1: Write the spec template**

Write `specs/_template.md`:

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
- [ ] Expected result 1
- [ ] Expected result 2

## Edge Cases
<!-- Known failure modes this test should NOT cover.
     Helps Claude stay scoped. Helps QA plan adjacent specs. -->

## Domain References
<!-- Which domain docs provide context for this test? -->
- Protocol: `domain/protocols/<name>.md`
- App: `domain/app/<name>.md`
```

- [ ] **Step 2: Remove old template**

```bash
rm specs/fe-qa-template.md
```

- [ ] **Step 3: Commit**

```bash
git add specs/_template.md
git rm specs/fe-qa-template.md
git commit -m "Replace spec template with structured _template.md"
```

---

### Task 4: Restructure existing spec to follow the new template

Move the existing spec into a feature subdirectory and rewrite it using the new template format. This serves as the example spec in the skeleton.

**Files:**
- Create: `specs/faucet/request-c2flr.md` (rewritten from template)
- Delete: `specs/successfully-request-c2flr.md` (moved + rewritten)

- [ ] **Step 1: Create feature directory and write spec in new format**

Write `specs/faucet/request-c2flr.md`:

```markdown
# Request C2FLR

## Context
Validates the core faucet functionality: a user can request testnet C2FLR tokens
and receive them on-chain.

## Preconditions
- Faucet application is accessible
- Coston2 RPC endpoint is reachable
- A fresh EVM address with zero balance

## Steps
1. Generate a new EVM address
2. Navigate to the Flare Faucet
3. Enter the EVM address in the address field
4. Click the "Request C2FLR" button

## Expected Results
- [ ] UI displays "Tokens sent" success message
- [ ] Address balance increases above 0 within 60 seconds

## Edge Cases
- Rate limiting (requesting twice with the same address) — separate spec
- Invalid address format — separate spec
- Network unavailable — separate spec

## Domain References
- Protocol: `domain/protocols/flare-faucet.md`
```

- [ ] **Step 2: Remove old spec**

```bash
rm specs/successfully-request-c2flr.md
```

- [ ] **Step 3: Commit**

```bash
git add specs/faucet/request-c2flr.md
git rm specs/successfully-request-c2flr.md
git commit -m "Restructure spec into feature subdirectory with new template format"
```

---

### Task 5: Create example domain knowledge — protocol doc

Write the Flare Faucet protocol doc as an example of how domain knowledge should be documented.

**Files:**
- Create: `domain/protocols/flare-faucet.md`

- [ ] **Step 1: Write protocol doc**

Write `domain/protocols/flare-faucet.md`:

```markdown
# Flare Faucet Protocol

## Overview
The faucet dispenses testnet C2FLR tokens on the Coston2 network. It provides
developers with free testnet tokens for development and testing purposes.

## Mechanics
- Sends a fixed amount of C2FLR to a provided EVM address
- Rate limited: one request per address per 24 hours
- Tokens are delivered via on-chain transaction (not instant)
- Typical confirmation time: 10-30 seconds

## Key Concepts
- **C2FLR**: Testnet token on Coston2 (not real value)
- **Coston2**: Flare's test network (chain ID 114)
- **EVM address**: Standard 0x-prefixed Ethereum-compatible address

## Endpoints
- Faucet UI: configured via `FLARE_FAUCET_URL` env var
- Coston2 RPC: configured via `COSTON2_RPC_URL` env var
```

- [ ] **Step 2: Remove .gitkeep from protocols (no longer needed)**

```bash
rm domain/protocols/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add domain/protocols/flare-faucet.md
git rm domain/protocols/.gitkeep
git commit -m "Add Flare Faucet protocol domain knowledge doc"
```

---

### Task 6: Create example domain knowledge — app doc

Write shared UI assumptions for the Flare Faucet app as an example.

**Files:**
- Create: `domain/app/flare-faucet-ui.md`

- [ ] **Step 1: Write app doc**

Write `domain/app/flare-faucet-ui.md`:

```markdown
# Flare Faucet UI Patterns

## Notifications
- Success: "Tokens sent" message displayed on screen after a successful request
- Pending: no explicit loading indicator documented yet

## Address Input
- Single text input field with placeholder "Flare address"
- Accepts standard EVM addresses (0x-prefixed, 42 characters)

## Token Display
- Amounts are not displayed in the faucet UI itself
- Balance verification happens on-chain via RPC, not through the UI
```

- [ ] **Step 2: Remove .gitkeep from app (no longer needed)**

```bash
rm domain/app/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add domain/app/flare-faucet-ui.md
git rm domain/app/.gitkeep
git commit -m "Add Flare Faucet UI patterns app domain doc"
```

---

### Task 7: Create example skill — transaction polling

Write a skill for the polling pattern used when verifying on-chain state after a UI action. This is a broadly applicable pattern across crypto QA projects.

**Files:**
- Create: `skills/transaction-polling.md`

- [ ] **Step 1: Write skill**

Write `skills/transaction-polling.md`:

```markdown
# Transaction Polling

## When to Use
When a test needs to verify an on-chain state change after a UI action (e.g.,
token transfer, contract interaction). The transaction is not instant — you
need to poll the chain until the expected state appears or a timeout is reached.

## Approach
Use a deadline-based polling loop with a sleep interval. Check the chain state
repeatedly until the expected condition is met or time runs out.

## Implementation Pattern
1. Record the current time and compute a deadline (e.g., 60 seconds from now)
2. Loop while current time < deadline:
   a. Query the chain for the expected state (e.g., balance > 0)
   b. If condition met, break
   c. Sleep for a short interval (e.g., 5 seconds)
3. After the loop, assert the expected state

```python
import time

deadline = time.time() + 60
while time.time() < deadline:
    if chain_client.get_balance(address) > 0:
        break
    time.sleep(5)

balance = chain_client.get_balance_ether(address)
assert balance > 0, f"Expected balance > 0, got {balance}"
```

## Gotchas
- Don't use a fixed number of retries — use a time-based deadline so the
  timeout is predictable regardless of sleep interval
- Keep the sleep interval reasonable (3-5 seconds) — too short hammers the
  RPC endpoint, too long wastes test time
- Always assert after the loop, not inside it — the loop is for waiting,
  the assertion is for verification
- Use `chain_client` from conftest.py fixtures, never create a new Web3
  instance in the test
```

- [ ] **Step 2: Remove .gitkeep from skills (no longer needed)**

```bash
rm skills/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add skills/transaction-polling.md
git rm skills/.gitkeep
git commit -m "Add transaction polling skill"
```

---

### Task 8: Update test function name to match spec naming convention

The file is already named `tests/test_request_c2flr.py`. Update the function name and docstring inside to match the new spec path.

**Files:**
- Modify: `tests/test_request_c2flr.py`

- [ ] **Step 1: Update test function name and docstring**

In `tests/test_request_c2flr.py`, rename `test_successfully_request_c2flr` to `test_request_c2flr`:

```python
# Before:
def test_successfully_request_c2flr(

# After:
def test_request_c2flr(
```

Also update the docstring to reference the new spec path:

```python
# Before:
"""Spec 1.1: Successfully Request C2FLR.

# After:
"""Spec: specs/faucet/request-c2flr.md
```

- [ ] **Step 2: Run tests to verify nothing broke**

```bash
pytest tests/test_request_c2flr.py --collect-only
```

Expected: test `test_request_c2flr` is collected.

- [ ] **Step 3: Commit**

```bash
git add tests/test_request_c2flr.py
git commit -m "Rename test function to match spec naming convention"
```

---

### Task 9: Update page object — remove assertion from FaucetPage

The design spec says page objects should return state, not assert. `FaucetPage.expect_success()` currently uses Playwright's `expect()`. Refactor it to return state so the test handles the assertion.

**Files:**
- Modify: `pages/faucet_page.py:24` — replace `expect_success` with a state-returning method
- Modify: `tests/test_request_c2flr.py` — update to assert on returned state

- [ ] **Step 1: Refactor FaucetPage to return state**

In `pages/faucet_page.py`, replace:

```python
def expect_success(self):
    expect(self.page.get_by_text("Tokens sent")).to_be_visible(timeout=30_000)
```

With:

```python
def get_success_message(self, timeout: int = 30_000) -> str | None:
    """Wait for and return the success message text, or None if not found."""
    msg = self.page.get_by_text("Tokens sent")
    try:
        msg.wait_for(state="visible", timeout=timeout)
        return msg.text_content()
    except TimeoutError:
        return None
```

Remove the `expect` import from the top of the file.

- [ ] **Step 2: Update test to assert on returned state**

In `tests/test_request_c2flr.py`, replace:

```python
faucet_page.expect_success()
```

With:

```python
success_message = faucet_page.get_success_message()
assert success_message is not None, "Expected 'Tokens sent' success message"
```

- [ ] **Step 3: Run test collection to verify**

```bash
pytest tests/test_request_c2flr.py --collect-only
```

Expected: test `test_request_c2flr` is collected without errors.

- [ ] **Step 4: Commit**

```bash
git add pages/faucet_page.py tests/test_request_c2flr.py
git commit -m "Refactor FaucetPage to return state instead of asserting"
```

---

### Task 10: Verify complete structure and final commit

Verify the skeleton matches the design spec's target structure.

**Files:**
- No new files

- [ ] **Step 1: Verify directory structure**

```bash
find . -not -path './.git/*' -not -path './.git' -not -path './uv.lock' -not -path './.devcontainer/*' -not -name '__pycache__' | sort
```

Expected structure should include:
- `./CLAUDE.md`
- `./README.md`
- `./domain/protocols/flare-faucet.md`
- `./domain/app/flare-faucet-ui.md`
- `./skills/transaction-polling.md`
- `./specs/_template.md`
- `./specs/faucet/request-c2flr.md`
- `./pages/base_page.py`
- `./pages/faucet_page.py`
- `./tests/test_request_c2flr.py`
- `./chain/client.py`
- `./conftest.py`

- [ ] **Step 2: Run full test collection**

```bash
pytest --collect-only
```

Expected: all tests collected successfully.

- [ ] **Step 3: Verify CLAUDE.md references are accurate**

Read CLAUDE.md and confirm all referenced directories and files exist.
