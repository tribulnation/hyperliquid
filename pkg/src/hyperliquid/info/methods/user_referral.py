from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class ReferredBy(TypedDict):
  referrer: str
  code: str

class ReferralTokenState(TypedDict):
  cumVlm: str
  unclaimedRewards: str
  claimedRewards: str
  builderRewards: str

class ReferralStateEntry(TypedDict):
  cumVlm: str
  cumRewardedFeesSinceReferred: str
  cumFeesRewardedToReferrer: str
  timeJoined: int
  user: str

class ReferrerData(TypedDict):
  code: str
  referralStates: list[ReferralStateEntry]

class ReferrerState(TypedDict):
  stage: str
  data: ReferrerData

class UserReferralResponse(TypedDict):
  referredBy: ReferredBy | None
  cumVlm: str
  unclaimedRewards: str
  claimedRewards: str
  builderRewards: str
  tokenToState: list[tuple[int, ReferralTokenState]]
  referrerState: ReferrerState | None
  rewardHistory: list[object]

adapter = pydantic.TypeAdapter(UserReferralResponse)

class UserReferral(InfoMixin):
  async def user_referral(self, user: str) -> UserReferralResponse:
    """Return a user's referral information.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-referral-information)
    """
    r = await self.request({'type': 'referral', 'user': user})
    return adapter.validate_python(r) if self.validate else r
