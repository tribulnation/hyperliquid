from typing_extensions import AsyncIterable
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

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

    - `coin`: Coin, e.g. "ETH".
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-historical-funding-rates)
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

    - `coin`: Coin, e.g. "ETH".
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-historical-funding-rates)
    """
    while end_time is None or start_time < end_time:
      fundings = await self.funding_history(coin, start_time, end_time=end_time)
      if not fundings:
        break
      yield fundings
      start_time = fundings[-1]['time'] + 1