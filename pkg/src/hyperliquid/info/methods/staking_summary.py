from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class StakingSummaryResponse(TypedDict):
  delegated: str
  undelegated: str
  totalPendingWithdrawal: str
  nPendingWithdrawals: int

adapter = pydantic.TypeAdapter(StakingSummaryResponse)

class StakingSummary(InfoMixin):
  async def staking_summary(self, user: str) -> StakingSummaryResponse:
    """Return a user's staking summary.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-staking-summary)
    """
    r = await self.request({'type': 'delegatorSummary', 'user': user})
    return adapter.validate_python(r) if self.validate else r
