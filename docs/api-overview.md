# API Overview

The package exposes four public entry points:

- `Info`
- `Exchange`
- `Streams`
- `Hyperliquid`

That split matches the actual transport and authentication model of Hyperliquid more closely than a single giant client.

## `Info`

Use `Info` for read-only request-response access.

```python
from hyperliquid import Info

async with Info.http() as info:
  mids = await info.all_mids()
```

Current coverage includes:

- general info endpoint methods like `all_mids`, `l2_book`, `candle_snapshot`, `open_orders`, `user_fills`
- perp reads like `perp_meta`, `perp_meta_and_asset_ctxs`, `funding_history`, `clearinghouse_state`
- spot reads like `spot_meta`, `spot_meta_and_asset_ctxs`, `spot_clearinghouse_state`

## `Exchange`

Use `Exchange` for signed actions.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
```

Current coverage includes:

- order placement and cancellation
- order modification
- leverage and isolated-margin updates
- transfers and withdrawals
- staking actions
- TWAP actions
- agent and abstraction actions

## `Streams`

Use `Streams` for subscriptions.

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  trades = await streams.trades('BTC')
```

Current coverage includes:

- public streams like `all_mids`, `l2_book`, `trades`, `bbo`, `candle`
- user streams like `user_fills`, `user_events`, `open_orders`, `user_fundings`

## `Hyperliquid`

Use `Hyperliquid` when you want `info`, `exchange`, and `streams` bundled together.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  mids = await client.info.all_mids()
```

Important nuance:

- `Hyperliquid.http()` and `Hyperliquid.ws()` require a wallet because `exchange` is always included
- for public-only workflows, prefer `Info` or `Streams`

## Generated Reference

The complete endpoint reference belongs under [Reference > API Reference](reference/api/index.md).
