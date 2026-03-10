from typing_extensions import Literal
import pydantic
from hyperliquid.info.core import InfoMixin

UserAbstractionResponse = Literal[
  'unifiedAccount',
  'portfolioMargin',
  'disabled',
  'default',
  'dexAbstraction',
]

adapter = pydantic.TypeAdapter(UserAbstractionResponse)

class UserAbstraction(InfoMixin):
  async def user_abstraction(self, user: str) -> UserAbstractionResponse:
    """Return a user's abstraction state.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-abstraction-state)
    """
    r = await self.request({'type': 'userAbstraction', 'user': user})
    return adapter.validate_python(r) if self.validate else r
