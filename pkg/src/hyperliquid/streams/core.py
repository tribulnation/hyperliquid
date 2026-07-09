from typing_extensions import Any, Callable
from dataclasses import dataclass
from datetime import timedelta
from hyperliquid.core import HYPERLIQUID_MAINNET, HYPERLIQUID_TESTNET
from hyperliquid.core.ws import SocketClient

@dataclass
class StreamsMixin:
  """Base mixin for Hyperliquid WebSocket stream endpoints."""
  client: SocketClient
  validate: bool = True

  @classmethod
  def of(cls, ws: SocketClient, *, validate: bool = True):
    """Create a Streams client from an existing WebSocket transport.

    Args:
      ws: Shared WebSocket transport.
      validate: Validate stream messages.
    """
    return cls(client=ws, validate=validate)

  @classmethod
  def new(
    cls, *, mainnet: bool = True, timeout: timedelta = timedelta(seconds=10),
    validate: bool = True, ws_url: str | None = None,
  ):
    """Create a Streams client with WebSocket transport.

    Args:
      mainnet: Use mainnet when true, testnet when false.
      timeout: WebSocket request timeout.
      validate: Validate stream messages.
      ws_url: Custom WebSocket URL. If provided, takes
        precedence over `mainnet`.
    """
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=ws_url or f'wss://{domain}/ws', timeout=timeout)
    return cls.of(ws, validate=validate)

  def subscribe(
    self, channel: str, params=None, *,
    request_channel: str | None = None,
    message_key: Callable[[Any], str] | None = None,
  ):
    """Subscribe to a stream, optionally separating request and message channels.

    `message_key`: for channels shared across multiple concurrent
    subscriptions (e.g. `l2Book`, tagged identically for every coin), a
    function deriving the local subscription key from an incoming
    notification. See `StreamsRpc.subscribe`.
    """
    return self.client.subscribe(
      channel, params, request_channel=request_channel, message_key=message_key,
    )

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)
