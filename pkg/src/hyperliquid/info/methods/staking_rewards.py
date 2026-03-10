from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class StakingReward(TypedDict):
  time: int
  source: str
  totalAmount: str

StakingRewardsResponse = list[StakingReward]

adapter = pydantic.TypeAdapter(StakingRewardsResponse)

class StakingRewards(InfoMixin):
  async def staking_rewards(self, user: str) -> StakingRewardsResponse:
    """Return a user's staking rewards.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-staking-rewards)
    """
    r = await self.request({'type': 'delegatorRewards', 'user': user})
    return adapter.validate_python(r) if self.validate else r
