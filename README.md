# Typed Hyperliquid

> A fully typed, validated async client for the Hyperliquid API.

**Use autocomplete instead of documentation.**

```python
from hyperliquid import Info

async with Info.http() as info:
  mids = await info.all_mids()
  print(mids['BTC'])
```

## Why Typed Hyperliquid?

- **🎯 Precise Types**: Strong typing throughout, so your editor can help before runtime does.
- **✅ Automatic Validation**: Catch upstream API changes earlier, where they are easier to debug.
- **⚡ Async First**: Built for concurrent, network-heavy workflows.
- **🔒 Safer Usage**: Typed inputs and explicit errors reduce avoidable mistakes.
- **🎨 Better DX**: Clear routing, sensible defaults, and minimal ceremony.
- **📦 Practical Extras**: HTTP, request-response WS, streams, and exchange actions under one package.

## Package Shape

This package exposes four public entry points:

- `Info` for read-only request-response access to the info endpoint
- `Exchange` for signed exchange actions
- `Streams` for WebSocket subscriptions
- `Hyperliquid` as a convenience bundle of all three

## Installation

```bash
pip install typed-hyperliquid
```

## Documentation

> [**Read the docs**](https://hyperliquid.tribulnation.com)
