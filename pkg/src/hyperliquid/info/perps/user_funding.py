from typing_extensions import AsyncIterable, Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin
from hyperliquid.info.pagination import paginate

PAGE_SIZE = 500
"""Maximum number of entries `user_funding` returns per call."""

class FundingDelta(TypedDict):
  type: Literal['funding']
  coin: str
  usdc: str
  """Funding paid or received (in USDC)."""
  szi: str
  """Size of the position (in base units)."""
  fundingRate: str
  """Funding rate (in relative units, e.g. 0.01 = 1%)."""
  nSamples: int | None

class UserFundingEntry(TypedDict):
  delta: FundingDelta
  hash: str
  time: int

adapter = pydantic.TypeAdapter(list[UserFundingEntry])

class UserFunding(InfoMixin):
  async def user_funding(
    self, user: str, start_time: int, *, end_time: int | None = None
  ) -> list[UserFundingEntry]:
    """Return a user's funding history.

    Args:
      user: Account address.
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
    """
    params: dict[str, object] = {
      'type': 'userFunding',
      'user': user,
      'startTime': start_time,
    }
    if end_time is not None:
      params['endTime'] = end_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r

  
  async def user_funding_paged(
    self, user: str, start_time: int, *, end_time: int | None = None
  ) -> AsyncIterable[list[UserFundingEntry]]:
    """Return a user's funding history, automatically paginating the results.

    A single call to `user_funding` returns at most 500 entries, so prefer this
    whenever the requested range may hold more.

    Every open position is funded on the same millisecond, so pages are advanced to
    the last timestamp seen rather than past it, and the re-fetched entries are
    dropped by position. Funding entries carry no unique id, so no key-based
    deduplication is possible.

    Args:
      user: Account address.
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    Raises:
      PaginationError: The range cannot be walked without losing entries. Notably,
        an account holding 500 or more funded positions cannot be swept at all,
        since one funding millisecond then fills a whole page.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
    """
    async def fetch(cursor: int) -> list[UserFundingEntry]:
      """Fetch one page of funding entries starting at `cursor`."""
      return await self.user_funding(user, cursor, end_time=end_time)
    async for page in paginate(
      fetch, start_time=start_time, end_time=end_time, page_size=PAGE_SIZE,
    ):
      yield page
