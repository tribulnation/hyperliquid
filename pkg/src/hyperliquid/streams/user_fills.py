from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

FillSide = Literal['A', 'B']
FillDir = Literal['Buy', 'Sell', 'Open Long', 'Close Long', 'Open Short', 'Close Short']

class FillLiquidation(TypedDict):
  liquidatedUser: NotRequired[str]
  markPx: float
  method: Literal['market', 'backstop']

class WsFill(TypedDict):
  coin: str
  px: str
  sz: str
  side: FillSide
  time: int
  startPosition: str
  dir: FillDir
  closedPnl: str
  hash: str
  oid: int
  crossed: bool
  fee: str
  tid: int
  liquidation: NotRequired[FillLiquidation]
  feeToken: str
  builderFee: NotRequired[str]
  twapId: NotRequired[int | None]

class WsUserFills(TypedDict):
  isSnapshot: NotRequired[bool]
  user: str
  fills: list[WsFill]

class UserFillsParams(TypedDict):
  user: str
  aggregateByTime: NotRequired[bool]

adapter = pydantic.TypeAdapter(WsUserFills)

class UserFills(StreamsMixin):
  async def user_fills(self, user: str, *, aggregate_by_time: bool | None = None):
    """Stream user fills.

    Args:
      user: Account address.
      aggregate_by_time: Aggregate partial fills in the same block.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions)
    """
    params: UserFillsParams = {'user': user}
    if aggregate_by_time is not None:
      params['aggregateByTime'] = aggregate_by_time
    stream = await self.subscribe('userFills', params)
    user_l = user.lower()
    stream = stream.filter(lambda msg: msg.get('user', '').lower() == user_l)
    def mapper(msg) -> WsUserFills:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
