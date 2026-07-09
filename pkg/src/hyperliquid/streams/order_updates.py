from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class WsBasicOrder(TypedDict):
  coin: str
  side: Literal['A', 'B']
  limitPx: str
  sz: str
  oid: int
  timestamp: int
  origSz: str
  cloid: NotRequired[str | None]

class WsOrder(TypedDict):
  order: WsBasicOrder
  status: Literal['open', 'filled', 'canceled', 'triggered', 'rejected', 'marginCanceled']
  statusTimestamp: int

OrderUpdatesData = list[WsOrder]

class OrderUpdatesParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(OrderUpdatesData)

class OrderUpdates(StreamsMixin):
  def order_updates(self, user: str):
    """Stream order updates for a user.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._order_updates_impl(user))

  async def _order_updates_impl(self, user: str):
    stream = await self.subscribe('orderUpdates', {'user': user})
    def mapper(msg) -> OrderUpdatesData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
