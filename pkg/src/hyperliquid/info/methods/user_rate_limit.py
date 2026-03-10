from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class UserRateLimitResponse(TypedDict):
  cumVlm: str
  """Cumulative volume."""
  nRequestsUsed: int
  """Requests used (cumulative minus reserved)."""
  nRequestsCap: int
  """Requests cap."""
  nRequestsSurplus: int
  """Requests surplus (reserved minus cumulative)."""

adapter = pydantic.TypeAdapter(UserRateLimitResponse)

class UserRateLimit(InfoMixin):
  async def user_rate_limit(self, user: str) -> UserRateLimitResponse:
    """Return rate limit info for a user.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-user-rate-limits)
    """
    r = await self.request({'type': 'userRateLimit', 'user': user})
    return adapter.validate_python(r) if self.validate else r
