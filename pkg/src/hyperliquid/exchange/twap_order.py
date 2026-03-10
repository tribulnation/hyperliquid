from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class TwapWire(TypedDict):
  a: int
  b: bool
  s: str
  r: bool
  m: int
  t: bool

class TwapOrderAction(TypedDict):
  type: Literal['twapOrder']
  twap: TwapWire

class TwapRunning(TypedDict):
  twapId: int

class TwapStatusRunning(TypedDict):
  running: TwapRunning

class TwapStatusError(TypedDict):
  error: str

TwapStatus = TwapStatusRunning | TwapStatusError

class TwapOrderData(TypedDict):
  status: TwapStatus

class TwapOrderResponse(TypedDict):
  type: Literal['twapOrder']
  data: TwapOrderData

adapter = pydantic.TypeAdapter(ExchangeResponse[TwapOrderResponse])

class TwapOrder(ExchangeMixin):
  async def twap_order(
    self, twap: TwapWire,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[TwapOrderResponse]:
    """Place a TWAP order.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#place-a-twap-order)
    """
    action: TwapOrderAction = {
      'type': 'twapOrder',
      'twap': twap,
    }
    ts = timestamp.now()
    sig = sign_l1_action(
      action,
      wallet=self.wallet,
      nonce=ts,
      mainnet=self.mainnet,
      vault_address=vault_address,
      expires_after=expires_after,
    )
    result = await self.client.request({
      'action': action,
      'nonce': ts,
      'signature': sig,
      'vaultAddress': vault_address,
      'expiresAfter': expires_after,
    })
    return adapter.validate_python(result) if self.validate else result
