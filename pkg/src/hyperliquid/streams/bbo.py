from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class L2BookLevel(TypedDict):
  px: str
  sz: str
  n: int

class BboData(TypedDict):
  coin: str
  time: int
  bbo: tuple[L2BookLevel | None, L2BookLevel | None]

class BboParams(TypedDict):
  coin: str

adapter = pydantic.TypeAdapter(BboData)

class Bbo(StreamsMixin):
  async def bbo(self, coin: str):
    """Stream best-bid-offer updates.

    - `coin`: Asset symbol.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('bbo', {'coin': coin})
    coin_l = coin.lower()
    stream = stream.filter(lambda msg: msg.get('coin', '').lower() == coin_l)
    def mapper(msg) -> BboData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
