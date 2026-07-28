from typing_extensions import AsyncIterable
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin
from hyperliquid.info.pagination import paginate

PAGE_SIZE = 500
"""Maximum number of entries `funding_history` returns per call."""

class FundingHistoryEntry(TypedDict):
  coin: str
  fundingRate: str
  premium: str
  time: int

adapter = pydantic.TypeAdapter(list[FundingHistoryEntry])

class FundingHistory(InfoMixin):
  async def funding_history(
    self, coin: str, start_time: int, *, end_time: int | None = None
  ) -> list[FundingHistoryEntry]:
    """Return historical funding rates, at most 500 entries. Use `funding_history_paged` for more.

    Args:
      coin: Coin, e.g. "ETH".
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-historical-funding-rates)
    """
    params: dict[str, object] = {
      'type': 'fundingHistory',
      'coin': coin,
      'startTime': start_time,
    }
    if end_time is not None:
      params['endTime'] = end_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r


  async def funding_history_paged(
    self, coin: str, start_time: int, *, end_time: int | None = None
  ) -> AsyncIterable[list[FundingHistoryEntry]]:
    """Return historical funding rates, automatically paginating the results.

    A single call to `funding_history` returns at most 500 entries, so prefer this
    whenever the requested range may hold more.

    Pages are advanced to the last timestamp seen rather than past it, and the
    re-fetched entries are dropped by position, so entries sharing a millisecond
    are never skipped at a page boundary.

    Args:
      coin: Coin, e.g. "ETH".
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    Raises:
      PaginationError: The range cannot be walked without losing entries.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-historical-funding-rates)
    """
    async def fetch(cursor: int) -> list[FundingHistoryEntry]:
      """Fetch one page of funding rates starting at `cursor`."""
      return await self.funding_history(coin, cursor, end_time=end_time)
    async for page in paginate(
      fetch, start_time=start_time, end_time=end_time, page_size=PAGE_SIZE,
    ):
      yield page
