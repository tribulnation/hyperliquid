from typing_extensions import AsyncIterable, Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

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

    - `user`: Account address.
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
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

    - `user`: Account address.
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.
    """
    while end_time is None or start_time < end_time:
      fundings = await self.user_funding(user, start_time, end_time=end_time)
      if not fundings:
        break
      yield fundings
      start_time = fundings[-1]['time'] + 1
