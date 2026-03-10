# Wallet Setup

Hyperliquid authentication in this client is wallet-based, not API-key based.

## Public Usage

No credentials are required for:

- `Info`
- `Streams`

## Authenticated Usage

`Exchange` and `Hyperliquid` sign requests with an Ethereum private key.

The simplest setup is:

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

Then:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
```

## Direct Wallet Usage

You can also pass a wallet or private key directly:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http('0xyour_private_key') as client:
  result = await client.exchange.noop()
```

## Exchange-Only Usage

If you only need signed actions, you can instantiate `Exchange` directly with a wallet object.

## Security Notes

- never commit your private key
- treat `HYPERLIQUID_PRIVATE_KEY` as a high-sensitivity secret
- keep public read workflows on `Info` or `Streams` whenever possible
- treat exchange examples as mainnet-sensitive unless you explicitly set `mainnet=False`
