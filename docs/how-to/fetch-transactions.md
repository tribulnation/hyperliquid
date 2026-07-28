# Fetch Your Transactions

Use `client.info` for account history reads. These methods take a user address and time windows in UTC milliseconds where applicable.

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
from hyperliquid import Hyperliquid

async with Hyperliquid.http(public=True) as client:
  fills = await client.info.user_fills_by_time(user, start_ms, end_time=end_ms)
  for fill in fills:
    print(fill['coin'], fill['side'], fill['px'], fill['sz'])
```

For large windows, use `user_fills_by_time_paged()`.

## Fetch Funding Payments

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http(public=True) as client:
  funding = await client.info.user_funding(user, start_ms, end_time=end_ms)
  for entry in funding:
    delta = entry['delta']
    print(delta['coin'], delta['usdc'], delta['fundingRate'])
```

For long ranges, use `user_funding_paged()`.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http(public=True) as client:
  async for chunk in client.info.user_funding_paged(user, start_ms, end_time=end_ms):
    print(len(chunk))
```

## Fetch Other Ledger Flows

Use `user_non_funding_ledger_updates()` for non-funding transfers and ledger events:
deposits, withdrawals, spot and sub-account transfers, vault flows, staking, liquidations,
and rewards.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http(public=True) as client:
  flows = await client.info.user_non_funding_ledger_updates(
    user,
    start_ms,
    end_time=end_ms,
  )
  for entry in flows:
    print(entry['time'], entry['delta']['type'])
```

Each `delta` is a union discriminated on `type`, so checking `type` narrows the entry to
the exact variant and its fields:

```python
for entry in flows:
  delta = entry['delta']
  if delta['type'] == 'deposit':
    print('deposited', delta['usdc'])
  elif delta['type'] == 'withdraw':
    print('withdrew', delta['usdc'], 'fee', delta['fee'])
  elif delta['type'] == 'send':
    print('sent', delta['amount'], delta['token'], 'to', delta['destination'])
  elif delta['type'] == 'vaultWithdraw':
    print('vault withdrawal', delta['netWithdrawnUsd'], 'from', delta['vault'])
```

All monetary amounts are `decimal.Decimal`, parsed from the exact decimal strings the API
returns, so no precision is lost. Never convert them to `float` for arithmetic.

Hyperliquid adds ledger types over time, and an unrecognized `type` raises a
`ValidationError` rather than validating as an opaque value. This is deliberate: ledger
deltas move balances, so a silently-ignored new type would corrupt any accounting built on
this endpoint. Failing loudly surfaces the new type so it can be modeled.

To tolerate unmodeled types, validate each delta individually and handle the failures
explicitly, rather than letting one unknown row abort a whole history read:

```python
from hyperliquid.info.perps.user_non_funding_ledger_updates import LedgerDelta
import pydantic

deltas = pydantic.TypeAdapter(LedgerDelta)

async with Info.http(validate=False) as info:
  for entry in await info.user_non_funding_ledger_updates(address, start_time):
    try:
      delta = deltas.validate_python(entry['delta'])
    except pydantic.ValidationError:
      handle_unknown(entry)  # log it, or surface it as an unclassified record
      continue
```

## Pagination

This endpoint returns **at most 2000 entries**, keeping the oldest and silently dropping
the rest -- no error, no indicator. Accounts with more history must be paginated:

```python
async def all_ledger_updates(info, address, start_time):
  while True:
    page = await info.user_non_funding_ledger_updates(address, start_time)
    if not page:
      return
    yield page
    if len(page) < 2000:
      return
    start_time = max(entry['time'] for entry in page) + 1
```

Note that `hash` is **not** unique: one transaction can emit several deltas, so `(time,
hash)` is not a primary key. Deduplicating on it will silently drop rows.
