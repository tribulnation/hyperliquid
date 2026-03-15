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

- **🎯 Precise Types**: Literal types where they help, so your IDE knows what is valid.
- **✅ Automatic Validation**: Catch upstream API changes earlier.
- **⚡ Async First**: Built for concurrent, network-heavy workflows.
- **🔒 Type Safety**: Full type hints throughout.
- **🎨 Better DX**: Clear routing, sensible defaults, optional complexity.
- **📦 Batteries Included**: HTTP, request-response WS, streams, and exchange actions when they earn their place.

## Installation

```bash
pip install typed-hyperliquid
```

## Quick Start

### Public reads

Use `Info` for public request-response access:

```python
from hyperliquid import Info

async with Info.http() as info:
  mids = await info.all_mids()
  book = await info.l2_book('BTC')
```

### Authenticated actions

Hyperliquid auth is wallet-based, not API-key based.

```bash
export HYPERLIQUID_PRIVATE_KEY="your_private_key"
```

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  result = await client.exchange.noop()
```

## Features

### No Unnecessary Imports

Notice something? **You never imported custom enum objects.** Just use the real values:

```python
from hyperliquid import Info

async with Info.http() as info:
  fills = await info.user_fills('0x...')
```

### Precise Type Annotations

Every field is precisely typed. You can work directly with validated response objects:

```python
from hyperliquid import Info

async with Info.http() as info:
  book = await info.l2_book('BTC')

coin: str = book['coin']
time: int = book['time']
```

### Automatic Validation

Response validation is **on by default** but can be disabled:

```python
validated = Info.http()
raw = Info.http(validate=False)
```

### HTTP, Request-Response WS, And Streams

The package intentionally separates three transport styles:

- `Info.http()` and `Exchange.http()` for normal HTTP usage
- `Info.ws()` and `Exchange.ws()` for request-response over WebSocket
- `Streams.new()` for subscriptions

### Composite Client

Use `Hyperliquid.http()` or `Hyperliquid.ws()` when you want `info`, `exchange`, and `streams` together:

```python
from hyperliquid import Hyperliquid

async with Hyperliquid.http() as client:
  mids = await client.info.all_mids()
```

## API Coverage

Current coverage is split across:

- `Info` for info endpoint methods, perp reads, spot reads, and account reads
- `Exchange` for signed exchange actions
- `Streams` for WebSocket subscriptions
- `Hyperliquid` as a convenience bundle of all three

📋 See [API Overview](api-overview.md) for the current structure and coverage.

## Documentation

- [**Getting Started**](getting-started.md) - Install the package and make your first requests
- [**Wallet Setup**](api-keys.md) - Configure wallet-based authentication
- [**API Overview**](api-overview.md) - Understand the client structure and coverage
- [**How To**](how-to/index.md) - Task-focused guides for orders, market data, balances, and transactions
- [**Reference**](reference/index.md) - Error handling, env vars, and generated endpoint docs

## Design Philosophy

Typed Hyperliquid follows the principles outlined in [this blog post](https://tribulnation.com/blog/clients).

*Details matter. Developer experience matters.*
