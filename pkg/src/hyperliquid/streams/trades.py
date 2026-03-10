from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class WsTrade(TypedDict):
  coin: str
  side: str
  px: str
  sz: str | int
  hash: str
  time: int
  tid: int
  users: tuple[str, str]

TradesData = list[WsTrade]

class TradesParams(TypedDict):
  coin: str

adapter = pydantic.TypeAdapter(TradesData)

class Trades(StreamsMixin):
  async def trades(self, coin: str):
    """Stream trades for a coin.

    - `coin`: Asset symbol.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('trades', {'coin': coin})
    coin_l = coin.lower()
    def match(msg):
      if not msg:
        return False
      first = msg[0] if isinstance(msg, list) else None
      if not isinstance(first, dict):
        return False
      return first.get('coin', '').lower() == coin_l
    stream = stream.filter(match)
    def mapper(msg) -> TradesData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
