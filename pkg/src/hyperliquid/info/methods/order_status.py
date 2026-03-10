from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class Order(TypedDict):
  coin: str
  side: Side
  """Order side."""
  limitPx: str
  """Limit price."""
  sz: str
  """Order size."""
  oid: int
  """Order id."""
  timestamp: int
  """Order timestamp (epoch ms)."""
  triggerCondition: str
  isTrigger: bool
  triggerPx: str
  children: list[object]
  isPositionTpsl: bool
  reduceOnly: bool
  orderType: str
  origSz: str
  """Original order size."""
  tif: Literal['Alo', 'Ioc', 'Gtc', 'FrontendMarket'] | None
  cloid: str | None
  """Client order id (16-byte hex string)."""

OrderStatus = Literal[
  'open',
  'filled',
  'canceled',
  'triggered',
  'rejected',
  'marginCanceled',
  'vaultWithdrawalCanceled',
  'openInterestCapCanceled',
  'selfTradeCanceled',
  'reduceOnlyCanceled',
  'siblingFilledCanceled',
  'delistedCanceled',
  'liquidatedCanceled',
  'scheduledCancel',
  'tickRejected',
  'minTradeNtlRejected',
  'perpMarginRejected',
  'reduceOnlyRejected',
  'badAloPxRejected',
  'iocCancelRejected',
  'badTriggerPxRejected',
  'marketOrderNoLiquidityRejected',
  'positionIncreaseAtOpenInterestCapRejected',
  'positionFlipAtOpenInterestCapRejected',
  'tooAggressiveAtOpenInterestCapRejected',
  'openInterestIncreaseRejected',
  'insufficientSpotBalanceRejected',
  'oracleRejected',
  'perpMaxPositionRejected',
]

class OrderStatusEntry(TypedDict):
  order: Order
  status: OrderStatus
  statusTimestamp: int
  """Status timestamp (epoch ms)."""

class OrderStatusResponseOrder(TypedDict):
  status: Literal['order']
  order: OrderStatusEntry

class OrderStatusResponseUnknown(TypedDict):
  status: Literal['unknownOid']

OrderStatusResponse = OrderStatusResponseOrder | OrderStatusResponseUnknown

adapter = pydantic.TypeAdapter(OrderStatusResponse)

class OrderStatusInfo(InfoMixin):
  async def order_status(
    self, user: str, oid: int | str
  ) -> OrderStatusResponse:
    """Return order status by order id or client order id.

    - `user`: Account address.
    - `oid`: Order id or 16-byte client order id hex string.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-order-status-by-oid-or-cloid)
    """
    r = await self.request({'type': 'orderStatus', 'user': user, 'oid': oid})
    return adapter.validate_python(r) if self.validate else r
