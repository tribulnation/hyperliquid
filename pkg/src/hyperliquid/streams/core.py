from dataclasses import dataclass
from datetime import timedelta
from hyperliquid.core import SocketClient, HYPERLIQUID_MAINNET, HYPERLIQUID_TESTNET

@dataclass
class StreamsMixin:
  client: SocketClient
  validate: bool = True

  @classmethod
  def of(cls, ws: SocketClient, *, validate: bool = True):
    return cls(client=ws, validate=validate)

  @classmethod
  def new(cls, *, mainnet: bool = True, timeout: timedelta = timedelta(seconds=10), validate: bool = True):
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=f'wss://{domain}/ws', timeout=timeout)
    return cls.of(ws, validate=validate)

  async def subscribe(self, channel: str, params=None):
    return await self.client.subscribe(channel, params)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)