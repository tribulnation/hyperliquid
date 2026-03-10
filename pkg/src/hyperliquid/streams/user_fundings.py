from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class WsUserFunding(TypedDict):
  time: int
  coin: str
  usdc: str
  szi: str
  fundingRate: str

class WsUserFundings(TypedDict, total=False):
  isSnapshot: bool
  user: str
  fundings: list[WsUserFunding]
  userFundings: list[WsUserFunding]

class UserFundingsParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WsUserFundings)

class UserFundings(StreamsMixin):
  async def user_fundings(self, user: str):
    """Stream user funding updates.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('userFundings', {'user': user})
    user_l = user.lower()
    def match(msg):
      if not isinstance(msg, dict):
        return True
      user_val = msg.get('user')
      return user_val is None or str(user_val).lower() == user_l
    stream = stream.filter(match)
    def mapper(msg) -> WsUserFundings:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
