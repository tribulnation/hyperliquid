# Listen To Public Data

Use `Streams` for public subscription-style updates.

## Listen To Order Book Updates

Use `l2_book()` for order book updates.

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  book = await streams.l2_book('BTC')
  async for update in book:
    best_bid = update['levels'][0][0]
    best_ask = update['levels'][1][0]
    print(best_bid['px'], best_ask['px'])
```

If you need more compact aggregation, use the optional `n_sig_figs` and `mantissa` arguments.

## Listen To Candle Updates

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  candles = await streams.candle('BTC', '1m')
  async for candle in candles:
    print(candle['s'], candle['i'], candle['c'])
```

## Listen To Market-Wide Mid Prices

```python
from hyperliquid import Streams

async with Streams.new() as streams:
  mids = await streams.all_mids()
  async for update in mids:
    print(update['mids']['BTC'])
```

## Other Public Streams

`Streams` also exposes:

- `l2_book()` for aggregated order book updates
- `candle()` for live candle updates
- `trades()` for public trade prints
- `all_mids()` for market-wide mid prices
- `bbo()` for best-bid/best-offer updates
- `active_asset_ctx()` and `active_asset_data()` for asset-level live state
