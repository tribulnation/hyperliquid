from typing_extensions import Literal, NotRequired, AsyncIterable
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class UserFill(TypedDict):
  coin: str
  """Asset being traded."""
  px: str
  """Fill price."""
  sz: str
  """Fill size."""
  side: Literal['A', 'B']
  """Fill side: 'B' (buy) or 'A' (ask i.e. sell)."""
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
  """Whether the fill crossed the spread. (i.e. whether it was a taker fill)"""
  fee: str
  """Total fee (inclusive of builder fee)."""
  tid: int
  """Trade id."""
  feeToken: str
  """Fee token."""
  builderFee: NotRequired[str]
  """Builder fee, when present."""

adapter = pydantic.TypeAdapter(list[UserFill])

class UserFillsByTime(InfoMixin):
  async def user_fills_by_time(
    self, user: str, start_time: int, *, end_time: int | None = None,
    aggregate_by_time: bool | None = None
  ) -> list[UserFill]:
    """Return a user's fills within a time range.

    - `user`: Account address.
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.
    - `aggregate_by_time`: Aggregate partial fills in the same block.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-fills-by-time)
    """
    params: dict[str, object] = {
      'type': 'userFillsByTime',
      'user': user,
      'startTime': start_time,
    }
    if end_time is not None:
      params['endTime'] = end_time
    if aggregate_by_time is not None:
      params['aggregateByTime'] = aggregate_by_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r


  async def user_fills_by_time_paged(
    self, user: str, start_time: int, *, end_time: int | None = None,
    aggregate_by_time: bool | None = None
  ) -> AsyncIterable[list[UserFill]]:
    """Return a user's fills within a time range, automatically paginating the results.

    - `user`: Account address.
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.
    - `aggregate_by_time`: Aggregate partial fills in the same block.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-fills-by-time)
    """
    while end_time is None or start_time < end_time:
      fills = await self.user_fills_by_time(user, start_time, end_time=end_time, aggregate_by_time=aggregate_by_time)
      if not fills:
        break
      yield fills
      start_time = fills[-1]['time'] + 1
