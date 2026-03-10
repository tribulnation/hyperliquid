from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class OpenOrder(TypedDict):
  coin: str
  """Asset being traded."""
  limitPx: str
  """Limit price."""
  oid: int
  """Order id."""
  side: Side
  """Order side."""
  sz: str
  """Order size."""
  origSz: str
  """Original order size."""
  timestamp: int
  """Order timestamp (epoch ms)."""

adapter = pydantic.TypeAdapter(list[OpenOrder])

class OpenOrders(InfoMixin):
  async def open_orders(
    self, user: str, *, dex: str | None = None
  ) -> list[OpenOrder]:
    """Return a user's open orders.

    - `user`: Account address.
    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-open-orders)
    """
    params = {'type': 'openOrders', 'user': user}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
