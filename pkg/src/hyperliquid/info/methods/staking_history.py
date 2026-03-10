from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class DelegationDelta(TypedDict):
  validator: str
  amount: str
  isUndelegate: bool

class StakingHistoryDelta(TypedDict):
  delegate: DelegationDelta

class StakingHistoryEntry(TypedDict):
  time: int
  hash: str
  delta: StakingHistoryDelta

StakingHistoryResponse = list[StakingHistoryEntry]

adapter = pydantic.TypeAdapter(StakingHistoryResponse)

class StakingHistory(InfoMixin):
  async def staking_history(self, user: str) -> StakingHistoryResponse:
    """Return a user's staking history.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-staking-history)
    """
    r = await self.request({'type': 'delegatorHistory', 'user': user})
    return adapter.validate_python(r) if self.validate else r
