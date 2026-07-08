from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class WsTrade(TypedDict):
  coin: str
  side: Literal['A', 'B']
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

    Args:
      coin: Asset symbol.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    coin_l = coin.lower()
    # See `l2_book.py` -- `trades` messages are tagged the same way
    # regardless of coin, so use a coin-specific local channel key. Trade
    # notifications are a list, so pull the coin from the first element.
    def message_key(data) -> str:
      first = data[0] if data else None
      trade_coin = first.get('coin') if isinstance(first, dict) else None
      return f'trades:{trade_coin.lower()}' if trade_coin is not None else 'trades'
    stream = await self.subscribe(
      f'trades:{coin_l}', {'coin': coin}, request_channel='trades', message_key=message_key,
    )
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
