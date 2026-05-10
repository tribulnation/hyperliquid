# Authenticated Setup

Hyperliquid authentication in this client is wallet-based, not API-key based.

Public reads and public streams can use `public=True` without credentials:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http(public=True) as client:
  mids = await client.info.all_mids()
```

## Environment Variable

For authenticated exchange actions, set your private key:

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

Then construct `Hyperliquid` normally:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
  print(result['status'])
```

For testnet, pass `mainnet=False` and set the testnet key:

```bash
export HYPERLIQUID_TESTNET_PRIVATE_KEY="your_testnet_private_key"
```

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http(mainnet=False) as client:
  result = await client.exchange.noop()
  print(result['status'])
```

## Direct Wallet Usage

You can also pass a private key or wallet object directly:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http('0xyour_private_key') as client:
  result = await client.exchange.noop()
  print(result['status'])
```

## Security Notes

- Never commit private keys.
- Treat `HYPERLIQUID_PRIVATE_KEY` and `HYPERLIQUID_TESTNET_PRIVATE_KEY` as high-sensitivity secrets.
- Treat exchange examples as mainnet-sensitive unless you explicitly set `mainnet=False`.
