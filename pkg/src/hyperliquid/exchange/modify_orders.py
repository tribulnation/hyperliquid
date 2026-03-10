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

class Modify(TypedDict):
  oid: int | str
  order: Order

class BatchModifyAction(TypedDict):
  type: Literal['batchModify']
  modifies: list[Modify]

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ModifyOrders(ExchangeMixin):
  async def modify_orders(
    self, *modifies: Modify,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Modify multiple orders.

    - `modifies`: Modify wire objects.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#modify-multiple-orders)
    """
    action: BatchModifyAction = {
      'type': 'batchModify',
      'modifies': list(modifies),
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
