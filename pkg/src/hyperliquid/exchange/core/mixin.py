from typing_extensions import Any, Mapping, Literal, Self, TypeVar, Generic
from hyperliquid.core import TypedDict
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
import pydantic
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from typed_core.exceptions import ApiError
from typed_core.http import HttpClient

from hyperliquid.core import (
  SocketClient,
  HYPERLIQUID_MAINNET, HYPERLIQUID_TESTNET,
)

T = TypeVar('T', default=Any)
Wallet = LocalAccount | str | bytes | int

def _parse_wallet(wallet: Wallet) -> LocalAccount:
  if isinstance(wallet, LocalAccount):
    return wallet
  else:
    return Account.from_key(wallet)

class ExchangeRequest(TypedDict):
  action: Mapping[str, Any]
  nonce: int
  signature: Mapping[str, Any]
  vaultAddress: str | None
  expiresAfter: int | None

class OkResponse(TypedDict, Generic[T]):
  status: Literal['ok']
  response: T

class ErrorResponse(TypedDict):
  status: Literal['err']
  response: Any

ExchangeResponse = OkResponse[T] | ErrorResponse

response_adapter = pydantic.TypeAdapter(ExchangeResponse)


@dataclass(kw_only=True)
class ExchangeClient(ABC):
  validate: bool = True

  @abstractmethod
  async def request(self, request: ExchangeRequest) -> ExchangeResponse:
    ...

  @abstractmethod
  async def __aenter__(self) -> Self:
    ...

  @abstractmethod
  async def __aexit__(self, exc_type, exc_value, traceback):
    ...


@dataclass(kw_only=True)
class ExchangeHttpClient(ExchangeClient):
  base_url: str
  http: HttpClient = field(default_factory=HttpClient)

  @property
  def url(self) -> str:
    return f'{self.base_url.rstrip("/")}/exchange'

  async def request(self, request: ExchangeRequest):
    r = await self.http.request('POST', self.url, json=request)
    if r.status_code != 200:
      raise ApiError(r.status_code, r.text)
    else:
      return response_adapter.validate_json(r.text) if self.validate else r.json()

  async def __aenter__(self):
    await self.http.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.http.__aexit__(exc_type, exc_value, traceback)


@dataclass(kw_only=True)
class ExchangeSocketClient(ExchangeClient):
  ws: SocketClient

  @property
  def url(self) -> str:
    return self.ws.url

  async def request(self, request: ExchangeRequest):
    reply = await self.ws.rpc_request({
      'type': 'action',
      'payload': request,
    })
    if reply['type'] == 'action':
      msg = reply['payload']
      return response_adapter.validate_python(msg) if self.validate else msg
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
class ExchangeMixin:
  client: ExchangeClient
  wallet: LocalAccount
  mainnet: bool
  validate: bool = True

  @classmethod
  def http(
    cls, wallet: Wallet, *, mainnet: bool = True, validate: bool = True,
    http: HttpClient | None = None, base_url: str | None = None,
  ):
    """Create an Exchange client with HTTP transport.

    Args:
      wallet: Private key or account object used to sign exchange actions.
      mainnet: Use mainnet when true, testnet when false.
      validate: Validate responses.
      http: Shared HTTP transport.
      base_url: Custom HTTP API root. If provided, takes
        precedence over `mainnet`.
    """
    wallet = _parse_wallet(wallet)
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    base_url = base_url or f'https://{domain}'
    http = http or HttpClient()
    client = ExchangeHttpClient(base_url=base_url, validate=validate, http=http)
    return cls(client=client, wallet=wallet, mainnet=mainnet, validate=validate)


  @classmethod
  def ws_of(cls, wallet: Wallet, *, ws: SocketClient, mainnet: bool = True, validate: bool = True):
    """Create an Exchange client from an existing WebSocket transport.

    Args:
      wallet: Private key or account object used to sign exchange actions.
      ws: Shared WebSocket transport.
      mainnet: Use mainnet signing rules when true,
        testnet signing rules when false.
      validate: Validate responses.
    """
    wallet = _parse_wallet(wallet)
    client = ExchangeSocketClient(ws=ws, validate=validate)
    return cls(client=client, wallet=wallet, mainnet=mainnet, validate=validate)

  @classmethod
  def ws(
    cls, wallet: Wallet, *, mainnet: bool = True, validate: bool = True,
    timeout: timedelta = timedelta(seconds=10), ws_url: str | None = None,
  ):
    """Create an Exchange client with WebSocket transport.

    Args:
      wallet: Private key or account object used to sign exchange actions.
      mainnet: Use mainnet when true, testnet when false.
      validate: Validate responses.
      timeout: WebSocket request timeout.
      ws_url: Custom WebSocket URL. If provided, takes
        precedence over `mainnet`.
    """
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=ws_url or f'wss://{domain}/ws', timeout=timeout)
    return cls.ws_of(wallet=wallet, ws=ws, mainnet=mainnet, validate=validate)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)
