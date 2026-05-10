# Environment Variables

## Public Usage

No environment variables are required for public reads or public streams.

## Authenticated Usage

The only environment variable currently used by the library itself is:

```bash
HYPERLIQUID_PRIVATE_KEY=
```

`Hyperliquid.http()` and `Hyperliquid.ws()` read `HYPERLIQUID_PRIVATE_KEY` if you do not pass a wallet explicitly.

## Networks

Network selection is configured through function arguments, not environment variables:

```python
from hyperliquid import Hyperliquid

client = Hyperliquid.http(mainnet=False)
```

There is no API key, API secret, or passphrase flow in the current implementation.
