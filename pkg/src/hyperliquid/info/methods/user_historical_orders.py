from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class HistoricalOrder(TypedDict):
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

HistoricalOrderStatus = Literal[
  'filled',
  'open',
  'canceled',
  'triggered',
  'rejected',
  'marginCanceled',
]

class HistoricalOrderEntry(TypedDict):
  order: HistoricalOrder
  status: HistoricalOrderStatus
  statusTimestamp: int
  """Status timestamp (epoch ms)."""

UserHistoricalOrdersResponse = list[HistoricalOrderEntry]

adapter = pydantic.TypeAdapter(UserHistoricalOrdersResponse)

class UserHistoricalOrders(InfoMixin):
  async def user_historical_orders(
    self, user: str
  ) -> UserHistoricalOrdersResponse:
    """Return a user's historical orders.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-historical-orders)
    """
    r = await self.request({'type': 'historicalOrders', 'user': user})
    return adapter.validate_python(r) if self.validate else r
