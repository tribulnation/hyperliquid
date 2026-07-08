from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class CrossLeverage(TypedDict):
  type: Literal['cross']
  value: int

class IsolatedLeverage(TypedDict):
  type: Literal['isolated']
  value: int
  rawUsd: str

Leverage = CrossLeverage | IsolatedLeverage

class ActiveAssetDataData(TypedDict):
  user: str
  coin: str
  leverage: Leverage
  maxTradeSzs: tuple[str, str]
  availableToTrade: tuple[str, str]
  markPx: NotRequired[str]

class ActiveAssetDataParams(TypedDict):
  user: str
  coin: str

adapter = pydantic.TypeAdapter(ActiveAssetDataData)

class ActiveAssetData(StreamsMixin):
  async def active_asset_data(self, user: str, coin: str):
    """Stream active asset data for a user.

    Args:
      user: Account address.
      coin: Asset symbol.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    user_l = user.lower()
    coin_l = coin.lower()
    # See `l2_book.py` -- `activeAssetData` messages are tagged the same way
    # regardless of user/coin, so use a user+coin-specific local channel key.
    stream = await self.subscribe(
      f'activeAssetData:{user_l}:{coin_l}', {'user': user, 'coin': coin}, request_channel='activeAssetData',
      message_key=lambda data: f'activeAssetData:{data["user"].lower()}:{data["coin"].lower()}',
    )
    def match(msg):
      return msg.get('user', '').lower() == user_l and msg.get('coin', '').lower() == coin_l
    stream = stream.filter(match)
    def mapper(msg) -> ActiveAssetDataData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
