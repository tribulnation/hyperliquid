# Listen To Your Trades

Use `Streams` for subscription-style updates.

## Listen To User Fills

`user_fills()` streams fills for a user address. This is the most direct way to listen to your trades.

```python
from hyperliquid import Streams

user = '0xYourAccountAddress'

async with Streams.new() as streams:
  fills = await streams.user_fills(user)
  async for update in fills:
    for fill in update['fills']:
      print(fill['coin'], fill['side'], fill['px'], fill['sz'])
```

If you want partial fills aggregated within the same block, pass `aggregate_by_time=True`.

```python
from hyperliquid import Streams

user = '0xYourAccountAddress'

async with Streams.new() as streams:
  fills = await streams.user_fills(user, aggregate_by_time=True)
  async for update in fills:
    print(update['fills'])
```

## Related User Streams

Depending on the workflow, these may also be useful:

- `order_updates()` for order lifecycle updates
- `open_orders()` for the current open-order view
- `user_events()` for a broader feed including fills, funding, and liquidations
