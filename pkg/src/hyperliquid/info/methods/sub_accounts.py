from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class MarginSummary(TypedDict):
  accountValue: str
  totalNtlPos: str
  """Total notional position."""
  totalRawUsd: str
  totalMarginUsed: str

class ClearinghouseState(TypedDict):
  marginSummary: MarginSummary
  crossMarginSummary: MarginSummary
  crossMaintenanceMarginUsed: str
  withdrawable: str
  assetPositions: list[object]
  time: int
  """State timestamp (epoch ms)."""

class SpotBalance(TypedDict):
  coin: str
  token: int
  total: str
  hold: str
  entryNtl: str
  """Entry notional."""

class SpotState(TypedDict):
  balances: list[SpotBalance]

class SubAccount(TypedDict):
  name: str
  subAccountUser: str
  master: str
  clearinghouseState: ClearinghouseState
  spotState: SpotState

SubAccountsResponse = list[SubAccount]

adapter = pydantic.TypeAdapter(SubAccountsResponse)

class SubAccounts(InfoMixin):
  async def sub_accounts(self, user: str) -> SubAccountsResponse:
    """Return a user's subaccounts.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-a-users-subaccounts)
    """
    r = await self.request({'type': 'subAccounts', 'user': user})
    return adapter.validate_python(r) if self.validate else r
