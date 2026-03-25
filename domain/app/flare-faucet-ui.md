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
