from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class StakingDelegation(TypedDict):
  validator: str
  amount: str
  lockedUntilTimestamp: int

StakingDelegationsResponse = list[StakingDelegation]

adapter = pydantic.TypeAdapter(StakingDelegationsResponse)

class StakingDelegations(InfoMixin):
  async def staking_delegations(self, user: str) -> StakingDelegationsResponse:
    """Return a user's staking delegations.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-staking-delegations)
    """
    r = await self.request({'type': 'delegations', 'user': user})
    return adapter.validate_python(r) if self.validate else r
