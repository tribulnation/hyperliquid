# Streams

Use `Streams` for subscription-style market data.

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  mids = await streams.all_mids()
  async for update in mids:
    print(update['mids']['BTC'])
```

Per-coin subscriptions are also available:

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  trades = await streams.trades('BTC')
  async for batch in trades:
    print(batch[0]['px'])
```

User streams such as `user_fills` are available too, but they still use an address rather than wallet signing.
