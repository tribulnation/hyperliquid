from typing_extensions import Mapping, Any, Self
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
from typed_core.exceptions import ApiError
from typed_core.http import HttpClient

from hyperliquid.core import (
  SocketClient,
  HYPERLIQUID_MAINNET, HYPERLIQUID_TESTNET,
)

class InfoClient(ABC):
  """Abstract transport for Hyperliquid info requests."""
  @abstractmethod
  async def request(self, params: Mapping[str, Any]):
    ...

  @abstractmethod
  async def __aenter__(self) -> Self:
    ...

  @abstractmethod
  async def __aexit__(self, exc_type, exc_value, traceback):
    ...


@dataclass(kw_only=True)
class InfoHttpClient(InfoClient):
  """HTTP transport for Hyperliquid info requests."""
  base_url: str
  http: HttpClient = field(default_factory=HttpClient)

  @property
  def url(self) -> str:
    return f'{self.base_url.rstrip("/")}/info'

  async def request(self, params: Mapping[str, Any]):
    r = await self.http.request('POST', self.url, json=params)
    if r.status_code != 200:
      raise ApiError(r.status_code, r.text)
    else:
      return r.json()

  async def __aenter__(self):
    await self.http.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)


@dataclass(kw_only=True)
class InfoSocketClient(InfoClient):
  """WebSocket transport for Hyperliquid info requests."""
  ws: SocketClient

  @property
  def url(self) -> str:
    return self.ws.url

  async def request(self, params: Mapping[str, Any]):
    reply = await self.ws.rpc_request({
      'type': 'info',
      'payload': params,
    })
    if reply['type'] == 'info':
      if reply['payload']['type'] == 'info':
        raise ApiError('Unexpected info reply type', reply['payload'])
      else:
        return reply['payload']['data']
    elif reply['type'] == 'error':
      raise ApiError(reply['payload'])
    else:
      raise ApiError(f'Unexpected reply type: {reply["type"]}', reply['payload'])

  async def __aenter__(self):
    await self.ws.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.ws.__aexit__(exc_type, exc_value, traceback)


@dataclass(kw_only=True)
class InfoMixin:
  """Base mixin for Hyperliquid info endpoint groups."""
  client: InfoClient
  validate: bool = True

  @classmethod
  def http(
    cls, *, mainnet: bool = True, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create an Info client with HTTP transport.

    Args:
      mainnet: Use mainnet when true, testnet when false.
      validate: Validate responses.
      http: Shared HTTP transport.
      base_url: Custom HTTP API root. If provided, takes
        precedence over `mainnet`.
    """
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    base_url = base_url or f'https://{domain}'
    http = http or HttpClient()
    return cls(client=InfoHttpClient(base_url=base_url, http=http), validate=validate)

  @classmethod
  def ws_of(cls, ws: SocketClient, *, validate: bool = True):
    """Create an Info client from an existing WebSocket transport.

    Args:
      ws: Shared WebSocket transport.
      validate: Validate responses.
    """
    return cls(client=InfoSocketClient(ws=ws), validate=validate)

  @classmethod
  def ws(
    cls, *, mainnet: bool = True, validate: bool = True,
    timeout: timedelta = timedelta(seconds=10), ws_url: str | None = None,
  ):
    """Create an Info client with WebSocket transport.

    Args:
      mainnet: Use mainnet when true, testnet when false.
      validate: Validate responses.
      timeout: WebSocket request timeout.
      ws_url: Custom WebSocket URL. If provided, takes
        precedence over `mainnet`.
    """
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=ws_url or f'wss://{domain}/ws', timeout=timeout)
    return cls.ws_of(ws, validate=validate)

  async def request(self, params: Mapping[str, Any]) -> Any:
    return await self.client.request(params)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)
