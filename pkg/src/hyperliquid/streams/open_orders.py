from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class OpenOrdersData(TypedDict):
  dex: str
  user: str
  orders: list[dict[str, object]]

class OpenOrdersParams(TypedDict):
  user: str
  dex: str

adapter = pydantic.TypeAdapter(OpenOrdersData)

class OpenOrders(StreamsMixin):
  def open_orders(self, user: str, dex: str):
    """Stream open orders for a user.

    Args:
      user: Account address.
      dex: Perp dex name.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._open_orders_impl(user, dex))

  async def _open_orders_impl(self, user: str, dex: str):
    stream = await self.subscribe('openOrders', {'user': user, 'dex': dex})
    user_l = user.lower()
    dex_l = dex.lower()
    def match(msg):
      return msg.get('user', '').lower() == user_l and msg.get('dex', '').lower() == dex_l
    stream = stream.filter(match)
    def mapper(msg) -> OpenOrdersData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
