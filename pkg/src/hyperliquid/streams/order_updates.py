from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class WsBasicOrder(TypedDict):
  coin: str
  side: str
  limitPx: str
  sz: str
  oid: int
  timestamp: int
  origSz: str
  cloid: NotRequired[str]

class WsOrder(TypedDict):
  order: WsBasicOrder
  status: str
  statusTimestamp: int

OrderUpdatesData = list[WsOrder]

class OrderUpdatesParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(OrderUpdatesData)

class OrderUpdates(StreamsMixin):
  async def order_updates(self, user: str):
    """Stream order updates for a user.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('orderUpdates', {'user': user})
    def mapper(msg) -> OrderUpdatesData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
