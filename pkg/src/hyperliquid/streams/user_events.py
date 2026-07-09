from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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

class WsUserFunding(TypedDict):
  time: int
  coin: str
  usdc: str
  szi: str
  fundingRate: str

class WsLiquidation(TypedDict):
  lid: int
  liquidator: str
  liquidated_user: str
  liquidated_ntl_pos: str
  liquidated_account_value: str

class WsNonUserCancel(TypedDict):
  coin: str
  oid: int

class WsUserEventFills(TypedDict):
  fills: list[WsFill]

class WsUserEventFunding(TypedDict):
  funding: WsUserFunding

class WsUserEventLiquidation(TypedDict):
  liquidation: WsLiquidation

class WsUserEventNonUserCancel(TypedDict):
  nonUserCancel: list[WsNonUserCancel]

WsUserEvent = WsUserEventFills | WsUserEventFunding | WsUserEventLiquidation | WsUserEventNonUserCancel

class UserEventsParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WsUserEvent)

class UserEvents(StreamsMixin):
  def user_events(self, user: str):
    """Stream user events.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._user_events_impl(user))

  async def _user_events_impl(self, user: str):
    stream = await self.subscribe('user', {'user': user}, request_channel='userEvents')
    def mapper(msg) -> WsUserEvent:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
