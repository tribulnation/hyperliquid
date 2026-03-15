# Fetch Your Transactions

Use `Info` for account history reads. These methods take a user address and time windows in UTC milliseconds where applicable.

```python
from datetime import datetime, timedelta
from hyperliquid.core import timestamp as ts

user = '0xYourAccountAddress'
end_ms = ts.now()
start_ms = ts.dump(datetime.now() - timedelta(days=7))
```

## Fetch Trades

Use `user_fills()` for recent fills or `user_fills_by_time()` for a specific window.

```python
from hyperliquid import Info

async with Info.http() as info:
  fills = await info.user_fills_by_time(user, start_ms, end_time=end_ms)
  for fill in fills:
    print(fill['coin'], fill['side'], fill['px'], fill['sz'])
```

For large windows, use `user_fills_by_time_paged()`.

## Fetch Funding Payments

```python
from hyperliquid import Info

async with Info.http() as info:
  funding = await info.user_funding(user, start_ms, end_time=end_ms)
  for entry in funding:
    delta = entry['delta']
    print(delta['coin'], delta['usdc'], delta['fundingRate'])
```

For long ranges, use `user_funding_paged()`.

## Fetch Other Ledger Flows

Use `user_non_funding_ledger_updates()` for non-funding transfers and ledger events.

```python
from hyperliquid import Info

async with Info.http() as info:
  flows = await info.user_non_funding_ledger_updates(
    user,
    start_ms,
    end_time=end_ms,
  )
  for entry in flows:
    print(entry['time'], entry['delta']['type'])
```
