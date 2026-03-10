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
  async def user_events(self, user: str):
    """Stream user events.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('userEvents', {'user': user})
    def mapper(msg) -> WsUserEvent:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
