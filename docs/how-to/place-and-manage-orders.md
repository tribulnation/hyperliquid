# Place & Manage Orders

Use `Exchange` for signed trading actions and `Info` for read-side order queries.

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

## Resolve The Asset Id

`Exchange.order()` takes one or more order wire objects, and each order uses Hyperliquid asset ids rather than coin symbols. For perps on the default dex, the asset id is the index in `perp_meta()['universe']`.

```python
from hyperliquid import Info

async with Info.http() as info:
  meta = await info.perp_meta()
  btc_asset = next(
    idx
    for idx, asset in enumerate(meta['universe'])
    if asset['name'] == 'BTC'
  )
```

## Place An Order

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.order({
    'a': btc_asset,
    'b': True,
    'p': '90000',
    's': '0.001',
    'r': False,
    't': {'limit': {'tif': 'Gtc'}},
  })

  status = result['response']['data']['statuses'][0]
  print(status)
```

You can pass multiple orders to `order(...)` in one call when you need batch placement.

## Query A Specific Order

Use the account address plus either an order id or a client order id.

```python
from hyperliquid import Info

user = '0xYourAccountAddress'
oid = 123456789

async with Info.http() as info:
  order = await info.order_status(user, oid)
  print(order)
```

## List Open Orders

`open_orders()` returns the compact wire shape. `frontend_open_orders()` includes extra fields such as trigger metadata. Both accept `dex=...` for non-default perp dexes.

```python
from hyperliquid import Info

user = '0xYourAccountAddress'

async with Info.http() as info:
  open_orders = await info.open_orders(user)
  print(len(open_orders))
```

## Cancel An Order

`cancel()` accepts one or more cancel wire objects with the same asset id plus the Hyperliquid order id.

```python
from hyperliquid import Hyperliquid

oid = 123456789

async with Hyperliquid.http() as client:
  result = await client.exchange.cancel({'a': btc_asset, 'o': oid})
  print(result['response']['data']['statuses'])
```

## Cancel All Open Orders

Hyperliquid exposes cancel-all as `schedule_cancel()`. Pass a UTC timestamp in milliseconds to arm it, or `None` to remove an existing schedule.

```python
from datetime import datetime, timedelta
from hyperliquid import Hyperliquid
from hyperliquid.core import timestamp as ts

cancel_at = ts.dump(datetime.now() + timedelta(seconds=30))

async with Hyperliquid.http() as client:
  result = await client.exchange.schedule_cancel(cancel_at)
  print(result['status'])
```
