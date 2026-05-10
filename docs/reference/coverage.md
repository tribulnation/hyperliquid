# Coverage

This page summarizes the public client surface in plain English. Use it to decide whether the package already covers your workflow before diving into the generated API reference.

## `client.info`

Read-only request-response access.

Current coverage includes:

- market-wide mids and order books
- candles and candle history
- perp metadata, asset contexts, funding, and dex status
- spot metadata and spot clearinghouse state
- user account state, fills, funding history, and ledger flows
- open orders, order status, subaccounts, and portfolio history

Use `client.info` for normal requests.

## `client.exchange`

Signed exchange actions.

Current coverage includes:

- placing and canceling orders
- modifying one or many existing orders
- schedule cancel
- leverage and isolated-margin updates
- spot, USDC, vault, and other transfer flows
- staking actions
- TWAP actions
- agent and abstraction actions

Use `client.exchange`.

## `client.streams`

Subscription-style WebSocket updates.

Current coverage includes:

- public trades, books, BBO, candles, and mids
- user fills and order updates
- open orders and user events
- user funding and non-funding ledger updates
- TWAP and account-state-related stream surfaces

Use `client.streams`.

## `Hyperliquid`

Convenience bundle of `info`, `exchange`, and `streams`.

Use this when you want one object that exposes all three surfaces. For public-only workflows, pass `public=True`.

## Generated Reference

For the exact method list and signatures, use [Reference > API](api/index.md).
