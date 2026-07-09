from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class WebData3UserState(TypedDict):
  agentAddress: str | None
  agentValidUntil: int | None
  serverTime: int
  cumLedger: float
  isVault: bool
  user: str
  optOutOfSpotDusting: NotRequired[bool]
  dexAbstractionEnabled: NotRequired[bool]

class LeadingVault(TypedDict):
  address: str
  name: str

class PerpDexState(TypedDict):
  totalVaultEquity: float
  perpsAtOpenInterestCap: NotRequired[list[str]]
  leadingVaults: NotRequired[list[LeadingVault]]

class WebData3Data(TypedDict):
  userState: WebData3UserState
  perpDexStates: list[PerpDexState]

class WebData3Params(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WebData3Data)

class WebData3(StreamsMixin):
  def web_data3(self, user: str):
    """Stream WebData3 updates for a user.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._web_data3_impl(user))

  async def _web_data3_impl(self, user: str):
    stream = await self.subscribe('webData3', {'user': user})
    user_l = user.lower()
    def match(msg):
      user_state = msg.get('userState') if isinstance(msg, dict) else None
      return isinstance(user_state, dict) and user_state.get('user', '').lower() == user_l
    stream = stream.filter(match)
    def mapper(msg) -> WebData3Data:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
