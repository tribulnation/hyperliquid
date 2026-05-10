# Typed Hyperliquid

> A fully typed, validated async client for the Hyperliquid API.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.ws(public=True) as client:
  stream = await client.streams.trades('BTC')
  async for msg in stream:
    for trade in msg:
      print(trade['px'], trade['sz'], trade['side'])
```

## Why Typed Hyperliquid?

- **🎯 Precise Types**: Typed endpoint inputs and responses.
- **✅ Runtime Validation**: Validated responses by default.
- **⚡ Async First**: HTTP, WebSocket RPC, and subscriptions.
- **📚 Full API Surface**: `client.info`, `client.exchange`, and `client.streams`.

## Installation

```bash
pip install typed-hyperliquid
```

## How To

- [Place & Manage Orders](how-to/place-and-manage-orders.md)
- [Fetch Market Data](how-to/fetch-market-data.md)
- [Fetch Your Balances & Positions](how-to/fetch-balances-and-positions.md)
- [Fetch Your Transactions](how-to/fetch-transactions.md)
- [Listen To Your Trades](how-to/listen-to-your-trades.md)
- [Listen To Public Data](how-to/listen-to-public-data.md)

## Reference

- [Authenticated Setup](authenticated-setup.md)
- [Error Handling](reference/error-handling.md)
- [Environment Variables](reference/env-vars.md)
- [Generated API Reference](reference/api/index.md)
