from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Side = Literal['A', 'B']

class UserFill(TypedDict):
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
  """Total fee (inclusive of builder fee)."""
  tid: int
  """Trade id."""
  feeToken: str
  """Fee token."""
  builderFee: NotRequired[str]
  """Builder fee, when present."""

UserFillsResponse = list[UserFill]

adapter = pydantic.TypeAdapter(UserFillsResponse)

class UserFills(InfoMixin):
  async def user_fills(
    self, user: str, *, aggregate_by_time: bool | None = None
  ) -> UserFillsResponse:
    """Return a user's most recent fills.

    - `user`: Account address.
    - `aggregate_by_time`: Aggregate partial fills in the same block.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-fills)
    """
    params: dict[str, object] = {'type': 'userFills', 'user': user}
    if aggregate_by_time is not None:
      params['aggregateByTime'] = aggregate_by_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
