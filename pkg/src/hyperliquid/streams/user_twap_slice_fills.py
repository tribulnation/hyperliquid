from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class FillLiquidation(TypedDict):
  liquidatedUser: NotRequired[str]
  markPx: float
  method: Literal['market', 'backstop']

class WsFill(TypedDict):
  coin: str
  px: str
  sz: str
  side: str
  time: int
  startPosition: str
  dir: str
  closedPnl: str
  hash: str
  oid: int
  crossed: bool
  fee: str
  tid: int
  liquidation: NotRequired[FillLiquidation]
  feeToken: str
  builderFee: NotRequired[str]

class WsTwapSliceFill(TypedDict):
  fill: WsFill
  twapId: int

class WsUserTwapSliceFills(TypedDict):
  isSnapshot: NotRequired[bool]
  user: str
  twapSliceFills: list[WsTwapSliceFill]

class UserTwapSliceFillsParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WsUserTwapSliceFills)

class UserTwapSliceFills(StreamsMixin):
  async def user_twap_slice_fills(self, user: str):
    """Stream TWAP slice fills for a user.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('userTwapSliceFills', {'user': user})
    user_l = user.lower()
    stream = stream.filter(lambda msg: msg.get('user', '').lower() == user_l)
    def mapper(msg) -> WsUserTwapSliceFills:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
