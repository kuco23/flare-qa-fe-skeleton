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
