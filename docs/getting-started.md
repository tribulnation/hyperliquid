# Getting Started

This guide gets you from installation to your first public and authenticated Hyperliquid requests.

## Install The Package

```bash
pip install typed-hyperliquid
```

## Make A Public HTTP Request

Use `Info` for public reads:

```python
from hyperliquid import Info

async with Info.http() as info:
  mids = await info.all_mids()
  book = await info.l2_book('BTC')
```

## Open A Public Stream

Use `Streams` for subscriptions:

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  trades = await streams.trades('BTC')
  async for batch in trades:
    print(batch[0]['px'])
```

## Make An Authenticated Request

Set your wallet private key:

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

Then use the composite client or `Exchange` directly:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
```

## Transport Choices

Use the surface that matches what you need:

- `Info.http()` for public request-response over HTTP
- `Info.ws()` for public request-response over WebSocket
- `Exchange.http()` or `Exchange.ws()` for signed actions
- `Streams.new()` for subscriptions
- `Hyperliquid.http()` or `Hyperliquid.ws()` for the full bundle

## Important Nuance

`Hyperliquid.http()` and `Hyperliquid.ws()` always require a wallet, because they include `exchange`.

For public-only workflows, prefer `Info` or `Streams` directly.

## Next Steps

- Read [Wallet Setup](api-keys.md) before using `Exchange` or `Hyperliquid`
- Read [API Overview](api-overview.md) to understand the split between `Info`, `Exchange`, `Streams`, and `Hyperliquid`
- Browse [Examples](examples/index.md) for practical workflows
