from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

@pydantic.with_config({'extra': 'allow'})
class LedgerDelta(TypedDict):
  type: str

class UserNonFundingLedgerEntry(TypedDict):
  delta: LedgerDelta
  hash: str
  time: int

UserNonFundingLedgerUpdatesResponse = list[UserNonFundingLedgerEntry]

adapter = pydantic.TypeAdapter(UserNonFundingLedgerUpdatesResponse)

class UserNonFundingLedgerUpdates(InfoMixin):
  async def user_non_funding_ledger_updates(
    self, user: str, start_time: int, *, end_time: int | None = None
  ) -> UserNonFundingLedgerUpdatesResponse:
    """Return a user's non-funding ledger updates.

    - `user`: Account address.
    - `start_time`: Start time in milliseconds, inclusive.
    - `end_time`: End time in milliseconds, inclusive.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
    """
    params: dict[str, object] = {
      'type': 'userNonFundingLedgerUpdates',
      'user': user,
      'startTime': start_time,
    }
    if end_time is not None:
      params['endTime'] = end_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
