from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class TwapState(TypedDict):
  coin: str
  user: str
  side: str
  sz: float
  executedSz: float
  executedNtl: float
  minutes: int
  reduceOnly: bool
  randomize: bool
  timestamp: int

class TwapStatus(TypedDict):
  status: Literal['activated', 'terminated', 'finished', 'error']
  description: str

class WsTwapHistory(TypedDict):
  state: TwapState
  status: TwapStatus
  time: int

class WsUserTwapHistory(TypedDict):
  isSnapshot: NotRequired[bool]
  user: str
  history: list[WsTwapHistory]

class UserTwapHistoryParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WsUserTwapHistory)

class UserTwapHistory(StreamsMixin):
  async def user_twap_history(self, user: str):
    """Stream TWAP history for a user.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('userTwapHistory', {'user': user})
    user_l = user.lower()
    stream = stream.filter(lambda msg: msg.get('user', '').lower() == user_l)
    def mapper(msg) -> WsUserTwapHistory:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
