from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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
  def bbo(self, coin: str):
    """Stream best-bid-offer updates.

    Args:
      coin: Asset symbol.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._bbo_impl(coin))

  async def _bbo_impl(self, coin: str):
    coin_l = coin.lower()
    # See `l2_book.py` -- `bbo` messages are tagged the same way regardless
    # of coin, so use a coin-specific local channel key.
    stream = await self.subscribe(
      f'bbo:{coin_l}', {'coin': coin}, request_channel='bbo',
      message_key=lambda data: f'bbo:{data["coin"].lower()}',
    )
    stream = stream.filter(lambda msg: msg.get('coin', '').lower() == coin_l)
    def mapper(msg) -> BboData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
