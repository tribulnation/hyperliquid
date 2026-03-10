from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

Role = Literal['missing', 'user', 'agent', 'vault', 'subAccount']

class UserRoleBase(TypedDict):
  role: Role

class UserRoleAgentData(TypedDict):
  user: str

class UserRoleAgent(UserRoleBase):
  role: Literal['agent'] # type: ignore
  data: UserRoleAgentData

class UserRoleSubAccountData(TypedDict):
  master: str

class UserRoleSubAccount(UserRoleBase):
  role: Literal['subAccount'] # type: ignore
  data: UserRoleSubAccountData

class UserRoleUser(UserRoleBase):
  role: Literal['user'] # type: ignore
  data: NotRequired[object]

class UserRoleVault(UserRoleBase):
  role: Literal['vault'] # type: ignore
  data: NotRequired[object]

class UserRoleMissing(UserRoleBase):
  role: Literal['missing'] # type: ignore
  data: NotRequired[object]

UserRoleResponse = (
  UserRoleAgent | UserRoleSubAccount | UserRoleUser | UserRoleVault | UserRoleMissing
)

adapter = pydantic.TypeAdapter(UserRoleResponse)

class UserRole(InfoMixin):
  async def user_role(self, user: str) -> UserRoleResponse:
    """Return a user's role.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-role)
    """
    r = await self.request({'type': 'userRole', 'user': user})
    return adapter.validate_python(r) if self.validate else r
