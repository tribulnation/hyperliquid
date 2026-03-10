from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class TwapFill(TypedDict):
  coin: str
  """Asset being traded."""
  px: str
  """Fill price."""
  sz: str
  """Fill size."""
  side: Side
  """Fill side."""
  time: int
  """Fill timestamp (epoch ms)."""
  startPosition: str
  """Position before the fill."""
  dir: str
  """Fill direction."""
  closedPnl: str
  """Closed PnL for the fill."""
  hash: str
  """Fill hash."""
  oid: int
  """Order id."""
  crossed: bool
  """Whether the fill crossed the spread."""
  fee: str
  """Total fee."""
  feeToken: str
  """Fee token."""
  tid: int
  """Trade id."""

class TwapSliceFill(TypedDict):
  fill: TwapFill
  twapId: int

UserTwapSliceFillsResponse = list[TwapSliceFill]

adapter = pydantic.TypeAdapter(UserTwapSliceFillsResponse)

class UserTwapSliceFills(InfoMixin):
  async def user_twap_slice_fills(
    self, user: str
  ) -> UserTwapSliceFillsResponse:
    """Return a user's TWAP slice fills.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-twap-slice-fills)
    """
    r = await self.request({'type': 'userTwapSliceFills', 'user': user})
    return adapter.validate_python(r) if self.validate else r
