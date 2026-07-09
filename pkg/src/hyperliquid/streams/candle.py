from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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
  def candle(self, coin: str, interval: str):
    """Stream candle updates for a coin.

    Args:
      coin: Asset symbol.
      interval: Candle interval.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._candle_impl(coin, interval))

  async def _candle_impl(self, coin: str, interval: str):
    coin_l = coin.lower()
    interval_l = interval.lower()
    # See `l2_book.py` -- `candle` messages are tagged the same way
    # regardless of coin/interval, so use a coin+interval-specific local
    # channel key.
    stream = await self.subscribe(
      f'candle:{coin_l}:{interval_l}', {'coin': coin, 'interval': interval}, request_channel='candle',
      message_key=lambda data: f'candle:{data["s"].lower()}:{data["i"].lower()}',
    )
    def match(msg):
      return msg.get('s', '').lower() == coin_l and msg.get('i', '').lower() == interval_l
    stream = stream.filter(match)
    def mapper(msg) -> CandleData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
