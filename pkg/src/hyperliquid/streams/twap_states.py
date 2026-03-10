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

class TwapStatesData(TypedDict):
  dex: str
  user: str
  states: list[tuple[int, TwapState]]

class TwapStatesParams(TypedDict):
  user: str
  dex: str

adapter = pydantic.TypeAdapter(TwapStatesData)

class TwapStates(StreamsMixin):
  async def twap_states(self, user: str, dex: str):
    """Stream TWAP states for a user.

    - `user`: Account address.
    - `dex`: Perp dex name.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('twapStates', {'user': user, 'dex': dex})
    user_l = user.lower()
    dex_l = dex.lower()
    def match(msg):
      return msg.get('user', '').lower() == user_l and msg.get('dex', '').lower() == dex_l
    stream = stream.filter(match)
    def mapper(msg) -> TwapStatesData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
