from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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
  def user_fundings(self, user: str):
    """Stream user funding updates.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._user_fundings_impl(user))

  async def _user_fundings_impl(self, user: str):
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
