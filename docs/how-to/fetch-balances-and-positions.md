# Fetch Your Balances & Positions

Use `Info` for account-state reads. These methods take a user address, not a signing wallet.

```python
user = '0xYourAccountAddress'
```

## Fetch Spot Balances

```python
from hyperliquid import Info

async with Info.http() as info:
  spot = await info.spot_clearinghouse_state(user)
  for balance in spot['balances']:
    print(balance['coin'], balance['total'])
```

## Fetch Perp Balances And Positions

`clearinghouse_state()` returns margin summaries plus open perpetual positions.

```python
from hyperliquid import Info

async with Info.http() as info:
  state = await info.clearinghouse_state(user)
  print(state['marginSummary']['accountValue'])

  for asset_position in state['assetPositions']:
    position = asset_position['position']
    print(position['coin'], position['szi'], position['entryPx'])
```

## Fetch Portfolio History

Use `user_portfolio()` for account-value and PnL history across the built-in periods.

```python
from hyperliquid import Info

async with Info.http() as info:
  portfolio = await info.user_portfolio(user)
  print(portfolio)
```

## Fetch Subaccounts

If the account uses subaccounts, `sub_accounts()` returns both perp and spot state for each one.

```python
from hyperliquid import Info

async with Info.http() as info:
  sub_accounts = await info.sub_accounts(user)
  print([account['name'] for account in sub_accounts])
```
