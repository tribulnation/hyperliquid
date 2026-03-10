# Authenticated Requests

Signed actions live under `Exchange`.

Set your wallet private key first:

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

A safe starter request is `noop()`:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
  print(result['status'])
```

Trading methods live under `client.exchange`, for example `order`, `cancel`, and `update_leverage`.

Notes:

- `Hyperliquid.http()` requires a wallet because it includes `exchange`
- signed requests are mainnet-sensitive unless you pass `mainnet=False`
- start with `noop()` or read-only flows before automating order placement
