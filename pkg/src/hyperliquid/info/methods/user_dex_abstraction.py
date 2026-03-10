import pydantic
from hyperliquid.info.core import InfoMixin

UserDexAbstractionResponse = bool

adapter = pydantic.TypeAdapter(UserDexAbstractionResponse)

class UserDexAbstraction(InfoMixin):
  async def user_dex_abstraction(self, user: str) -> UserDexAbstractionResponse:
    """Return a user's HIP-3 DEX abstraction state.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-hip-3-dex-abstraction-state)
    """
    r = await self.request({'type': 'userDexAbstraction', 'user': user})
    return adapter.validate_python(r) if self.validate else r
