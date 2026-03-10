from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

TimeInForce = Literal['Alo', 'Ioc', 'Gtc']
"""Time in force.
- `Alo`: Add liquidity only (i.e. post only).
- `Ioc`: Immediate or cancel.
- `Gtc`: Good til canceled.
"""

class LimitDetails(TypedDict):
  tif: TimeInForce
  """Time in force.
- `Alo`: Add liquidity only (i.e. post only).
- `Ioc`: Immediate or cancel.
- `Gtc`: Good til canceled.
"""

class LimitType(TypedDict):
  limit: LimitDetails

class TriggerDetails(TypedDict):
  triggerPx: float
  """Trigger price."""
  isMarket: bool
  """Whether to execute as market order when the trigger price is hit."""
  tpsl: Literal['tp', 'sl']
  """Take profit or stop loss."""

class TriggerType(TypedDict):
  trigger: TriggerDetails

OrderType = LimitType | TriggerType

class Order(TypedDict):
  a: int
  """Asset index."""
  b: bool
  """True for buy, false for sell."""
  p: str
  """Limit price."""
  s: str
  """Order size."""
  r: bool
  """Reduce-only flag."""
  t: OrderType
  c: NotRequired[str]
  """Client order id (16-byte hex string)."""

def reorder(order: Order) -> Order:
  """The dict must have this specific key order for signing to work."""
  new_order: Order = {
    'a': order['a'],
    'b': order['b'],
    'p': order['p'],
    's': order['s'],
    'r': order['r'],
    't': order['t'],
  }
  if 'c' in order:
    new_order['c'] = order['c']
  return new_order

Grouping = Literal['na', 'normalTpsl', 'positionTpsl']

class BuilderInfo(TypedDict):
  b: str
  """The public address of the builder."""
  f: int
  """The amount of the fee in tenths of basis points (e.g., 10 means 1 basis point)."""

class RestingStatus(TypedDict):
  oid: int
  """Order id."""

class FilledStatus(TypedDict):
  totalSz: str
  """Total filled size."""
  avgPx: str
  """Average fill price."""
  oid: int
  """Order id."""

class OrderStatusResting(TypedDict):
  resting: RestingStatus

class OrderStatusFilled(TypedDict):
  filled: FilledStatus

class OrderStatusError(TypedDict):
  error: str

OrderStatus = OrderStatusResting | OrderStatusFilled | OrderStatusError

class OrderResponseData(TypedDict):
  statuses: list[OrderStatus]

class OrderResponse(TypedDict):
  type: Literal['order']
  data: OrderResponseData

adapter = pydantic.TypeAdapter(ExchangeResponse[OrderResponse])

class PlaceOrder(ExchangeMixin):
  async def order(
    self, *orders: Order, grouping: Grouping = 'na',
    builder: BuilderInfo | None = None,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[OrderResponse]:
    action = {
      'type': 'order',
      'orders': [reorder(order) for order in orders],
      'grouping': grouping,
    }
    if builder:
      action['builder'] = builder
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
