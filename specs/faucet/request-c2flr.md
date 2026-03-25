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
