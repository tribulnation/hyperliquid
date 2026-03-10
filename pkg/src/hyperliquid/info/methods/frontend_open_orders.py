from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class FrontendOpenOrder(TypedDict):
  coin: str
  """Asset being traded."""
  isPositionTpsl: bool
  """Whether the order is a position TP/SL."""
  isTrigger: bool
  """Whether the order is a trigger order."""
  limitPx: str
  """Limit price."""
  oid: int
  """Order id."""
  orderType: str
  """Order type, e.g. Limit."""
  origSz: str
  """Original order size."""
  reduceOnly: bool
  """Whether the order only reduces position size."""
  side: Side
  """Order side."""
  sz: str
  """Current order size."""
  timestamp: int
  """Order timestamp (epoch ms)."""
  triggerCondition: str
  """Trigger condition."""
  triggerPx: str
  """Trigger price."""

FrontendOpenOrdersResponse = list[FrontendOpenOrder]

adapter = pydantic.TypeAdapter(FrontendOpenOrdersResponse)

class FrontendOpenOrders(InfoMixin):
  async def frontend_open_orders(
    self, user: str, *, dex: str | None = None
  ) -> FrontendOpenOrdersResponse:
    """Return open orders with additional frontend info.

    - `user`: Account address.
    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-open-orders-with-additional-frontend-info)
    """
    params = {'type': 'frontendOpenOrders', 'user': user}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
