# Fetch Market Data

Use `Info` for request-response market data reads.

## Fetch Depth

```python
from hyperliquid import Info

async with Info.http() as info:
  book = await info.l2_book('BTC')
  best_bid = book['levels'][0][0]
  best_ask = book['levels'][1][0]
  print(best_bid['px'], best_ask['px'])
```

## Fetch Candles

```python
from datetime import datetime, timedelta
from hyperliquid import Info
from hyperliquid.core import timestamp as ts

end_time = ts.now()
start_time = ts.dump(datetime.now() - timedelta(hours=1))

async with Info.http() as info:
  candles = await info.candle_snapshot(
    coin='BTC',
    interval='1m',
    start_time=start_time,
    end_time=end_time,
  )
  print(candles[-1]['c'])
```

## Fetch Current Funding

For the current funding snapshot, `perp_meta_and_asset_ctxs()` returns metadata and live asset contexts together.

```python
from hyperliquid import Info

async with Info.http() as info:
  meta, contexts = await info.perp_meta_and_asset_ctxs()
  current_funding = {
    asset['name']: ctx['funding']
    for asset, ctx in zip(meta['universe'], contexts)
  }
  print(current_funding['BTC'])
```

If you want the venue-wide next funding snapshot instead, use `predicted_fundings()`.

## Fetch Funding History

```python
from datetime import datetime, timedelta
from hyperliquid import Info
from hyperliquid.core import timestamp as ts

end_time = ts.now()
start_time = ts.dump(datetime.now() - timedelta(days=7))

async with Info.http() as info:
  history = await info.funding_history(
    'BTC',
    start_time,
    end_time=end_time,
  )
  print(history[-1]['fundingRate'])
```

For longer windows, use `funding_history_paged()`.
