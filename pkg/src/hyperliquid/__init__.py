from dataclasses import dataclass as _dataclass
import asyncio as _asyncio
from eth_account.account import Account as _Account
from eth_account.signers.local import LocalAccount
from .core import HYPERLIQUID_MAINNET, HYPERLIQUID_TESTNET
from .info import Info
from .exchange import Exchange
from .streams import Streams

Wallet = LocalAccount | str | bytes | int

def _env_wallet() -> LocalAccount:
  import os
  if (pk := os.getenv('HYPERLIQUID_PRIVATE_KEY')) is None:
    raise ValueError('HYPERLIQUID_PRIVATE_KEY is not set. Either set it or provide the `wallet` argument.')
  return _Account.from_key(pk)

def _parse_wallet(wallet: Wallet | None) -> LocalAccount:
  if wallet is None:
    return _env_wallet()
  if isinstance(wallet, LocalAccount):
    return wallet
  else:
    return _Account.from_key(wallet)

@_dataclass
class Hyperliquid:
  info: Info
  exchange: Exchange
  streams: Streams

  @classmethod
  def http(cls, wallet: Wallet | None = None, /, *, mainnet: bool = True, validate: bool = True):
    wallet = _parse_wallet(wallet)
    from .core import HttpClient
    http = HttpClient()
    return cls(
      info=Info.http(mainnet=mainnet, validate=validate, http=http),
      exchange=Exchange.http(wallet, mainnet=mainnet, validate=validate, http=http),
      streams=Streams.new(mainnet=mainnet, validate=validate),
    )

  @classmethod
  def ws(cls, wallet: Wallet | None = None, *, mainnet: bool = True, validate: bool = True):
    wallet = _parse_wallet(wallet)
    from .core import SocketClient
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=f'wss://{domain}/ws')
    return cls(
      info=Info.ws_of(ws, validate=validate),
      exchange=Exchange.ws_of(wallet, ws=ws, mainnet=mainnet, validate=validate),
      streams=Streams.of(ws, validate=validate),
    )


  async def __aenter__(self):
    await _asyncio.gather(
      self.info.__aenter__(),
      self.exchange.__aenter__(),
      self.streams.__aenter__(),
    )
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await _asyncio.gather(
      self.info.__aexit__(exc_type, exc_value, traceback),
      self.exchange.__aexit__(exc_type, exc_value, traceback),
      self.streams.__aexit__(exc_type, exc_value, traceback),
    )