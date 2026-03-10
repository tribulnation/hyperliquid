# Public Data

Start with `Info` for public request-response data.

```python
from hyperliquid import Info

async with Info.http() as info:
  mids = await info.all_mids()
  book = await info.l2_book('BTC')
  print(mids['BTC'])
  print(book['levels'][0][0]['px'])
```

Candle snapshots use millisecond timestamps:

```python
from datetime import datetime, timedelta, timezone
from hyperliquid import Info

end = datetime.now(timezone.utc)
start = end - timedelta(hours=1)

async with Info.http() as info:
  candles = await info.candle_snapshot(
    coin='BTC',
    interval='1m',
    start_time=int(start.timestamp() * 1000),
    end_time=int(end.timestamp() * 1000),
  )
```
