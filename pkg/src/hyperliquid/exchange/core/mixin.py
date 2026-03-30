from typing_extensions import Any, Mapping, Literal, Self, TypeVar, Generic
from hyperliquid.core import TypedDict
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
import pydantic
from eth_account.account import Account
from eth_account.signers.local import LocalAccount

from hyperliquid.core import (
  HttpClient, SocketClient, ApiError,
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
  domain: str
  http: HttpClient = field(default_factory=HttpClient)

  @property
  def url(self) -> str:
    return f'https://{self.domain}/exchange'

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
  def http(cls, wallet: Wallet, *, mainnet: bool = True, validate: bool = True, http: HttpClient | None = None):
    wallet = _parse_wallet(wallet)
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    http = http or HttpClient()
    client = ExchangeHttpClient(domain=domain, validate=validate, http=http)
    return cls(client=client, wallet=wallet, mainnet=mainnet, validate=validate)


  @classmethod
  def ws_of(cls, wallet: Wallet, *, ws: SocketClient, mainnet: bool = True, validate: bool = True):
    wallet = _parse_wallet(wallet)
    client = ExchangeSocketClient(ws=ws, validate=validate)
    return cls(client=client, wallet=wallet, mainnet=mainnet, validate=validate)

  @classmethod
  def ws(cls, wallet: Wallet, *, mainnet: bool = True, validate: bool = True, timeout: timedelta = timedelta(seconds=10)):
    domain = HYPERLIQUID_MAINNET if mainnet else HYPERLIQUID_TESTNET
    ws = SocketClient(url=f'wss://{domain}/ws', timeout=timeout)
    return cls.ws_of(wallet=wallet, ws=ws, mainnet=mainnet, validate=validate)

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)
