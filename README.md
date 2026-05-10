# Typed Hyperliquid

[![PyPI version](https://img.shields.io/pypi/v/typed-hyperliquid.svg)](https://pypi.org/project/typed-hyperliquid/)
[![Python versions](https://img.shields.io/pypi/pyversions/typed-hyperliquid.svg)](https://pypi.org/project/typed-hyperliquid/)
[![Docs](https://img.shields.io/badge/docs-live-black)](https://hyperliquid.tribulnation.com/)
[![License](https://img.shields.io/pypi/l/typed-hyperliquid.svg)](LICENSE)


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tribulnation/hyperliquid/refs/heads/main/media/hyperliquid-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tribulnation/hyperliquid/refs/heads/main/media/hyperliquid-light.svg">
  <img alt="Hyperliquid" src="https://raw.githubusercontent.com/tribulnation/hyperliquid/refs/heads/main/media/hyperliquid-light.svg">
</picture>

> A fully typed, validated async client for the Hyperliquid API.

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.ws(public=True) as client:
  stream = await client.streams.trades('BTC')
  async for msg in stream:
    for trade in msg:
      print(trade['px'], trade['sz'], trade['side'])
```

## Why Typed Hyperliquid?

- **🎯 Precise Types**: Typed endpoint inputs and responses.
- **✅ Runtime Validation**: Validated responses by default.
- **⚡ Async First**: HTTP, WebSocket RPC, and subscriptions.
- **📚 Full API Surface**: `client.info`, `client.exchange`, and
  `client.streams`.

## Installation

```bash
pip install typed-hyperliquid
```

For authenticated exchange actions, set a private key:

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

## Overview

Typed Hyperliquid exposes the upstream API as three client surfaces:

- `client.info`: public and account read methods like `all_mids`, `l2_book`,
  `clearinghouse_state`, `user_fills`, and spot/perp metadata.
- `client.exchange`: signed actions like placing orders, canceling orders,
  transfers, withdrawals, staking, TWAPs, and leverage updates.
- `client.streams`: WebSocket subscriptions like trades, books, candles,
  user fills, user events, and open orders.

Use `Hyperliquid.http()` or `Hyperliquid.ws()` depending on the transport you
want for request-response methods:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  mids = await client.info.all_mids()
  result = await client.exchange.noop()
```

For testnet, pass `mainnet=False` and set `HYPERLIQUID_TESTNET_PRIVATE_KEY`.

## Documentation

- [**Read the docs**](https://hyperliquid.tribulnation.com)
- [Getting Started](https://hyperliquid.tribulnation.com/getting-started/)
- [API Overview](https://hyperliquid.tribulnation.com/api-overview/)
- [API Keys / Wallet Setup](https://hyperliquid.tribulnation.com/api-keys/)
