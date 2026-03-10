from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

TimeInForce = Literal['Alo', 'Ioc', 'Gtc']

class LimitDetails(TypedDict):
  tif: TimeInForce

class LimitType(TypedDict):
  limit: LimitDetails

class TriggerDetails(TypedDict):
  triggerPx: float
  isMarket: bool
  tpsl: Literal['tp', 'sl']

class TriggerType(TypedDict):
  trigger: TriggerDetails

OrderType = LimitType | TriggerType

class Order(TypedDict):
  a: int
  b: bool
  p: str
  s: str
  r: bool
  t: OrderType
  c: NotRequired[str]

class ModifyOrderAction(TypedDict):
  type: Literal['modify']
  oid: int | str
  order: Order

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ModifyOrder(ExchangeMixin):
  async def modify_order(
    self, oid: int | str, order: Order,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Modify a single order.

    - `oid`: Order id or cloid.
    - `order`: Order wire object.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#modify-an-order)
    """
    action: ModifyOrderAction = {
      'type': 'modify',
      'oid': oid,
      'order': order,
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
