from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class UserVaultEquity(TypedDict):
  vaultAddress: str
  equity: str

UserVaultEquitiesResponse = list[UserVaultEquity]

adapter = pydantic.TypeAdapter(UserVaultEquitiesResponse)

class UserVaultEquities(InfoMixin):
  async def user_vault_equities(
    self, user: str
  ) -> UserVaultEquitiesResponse:
    """Return a user's vault equities.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-vault-deposits)
    """
    r = await self.request({'type': 'userVaultEquities', 'user': user})
    return adapter.validate_python(r) if self.validate else r
