from typing_extensions import NotRequired, Any
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class DailyUserVlm(TypedDict):
  date: str
  userCross: str
  userAdd: str
  exchange: str

class VipTier(TypedDict):
  ntlCutoff: str
  cross: str
  add: str
  spotCross: str
  spotAdd: str

class MmTier(TypedDict):
  makerFractionCutoff: str
  add: str

class FeeTiers(TypedDict):
  vip: list[VipTier]
  mm: list[MmTier]

class StakingDiscountTier(TypedDict):
  bpsOfMaxSupply: str
  discount: str

class FeeSchedule(TypedDict):
  cross: str
  add: str
  spotCross: str
  spotAdd: str
  tiers: FeeTiers
  referralDiscount: str
  stakingDiscountTiers: list[StakingDiscountTier]

class StakingLink(TypedDict):
  type: str
  stakingUser: str

class ActiveStakingDiscount(TypedDict):
  bpsOfMaxSupply: str
  discount: str

class UserFeesResponse(TypedDict):
  dailyUserVlm: list[DailyUserVlm]
  feeSchedule: FeeSchedule
  userCrossRate: str
  userAddRate: str
  userSpotCrossRate: str
  userSpotAddRate: str
  activeReferralDiscount: str
  trial: Any | None
  feeTrialReward: NotRequired[str]
  nextTrialAvailableTimestamp: int | None
  stakingLink: StakingLink | None
  activeStakingDiscount: ActiveStakingDiscount | None

adapter = pydantic.TypeAdapter(UserFeesResponse)

class UserFees(InfoMixin):
  async def user_fees(self, user: str) -> UserFeesResponse:
    """Return a user's fee schedule and rates.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-fees)
    """
    r = await self.request({'type': 'userFees', 'user': user})
    return adapter.validate_python(r) if self.validate else r
