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
