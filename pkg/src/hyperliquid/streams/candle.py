from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class CandleData(TypedDict):
  t: int
  T: int
  s: str
  i: str
  o: float | str
  c: float | str
  h: float | str
  l: float | str
  v: float | str
  n: int

class CandleParams(TypedDict):
  coin: str
  interval: str

adapter = pydantic.TypeAdapter(CandleData)

class Candle(StreamsMixin):
  async def candle(self, coin: str, interval: str):
    """Stream candle updates for a coin.

    - `coin`: Asset symbol.
    - `interval`: Candle interval.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('candle', {'coin': coin, 'interval': interval})
    coin_l = coin.lower()
    interval_l = interval.lower()
    def match(msg):
      return msg.get('s', '').lower() == coin_l and msg.get('i', '').lower() == interval_l
    stream = stream.filter(match)
    def mapper(msg) -> CandleData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
