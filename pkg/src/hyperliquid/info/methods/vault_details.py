from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

PortfolioPeriod = Literal[
  'day',
  'week',
  'month',
  'allTime',
  'perpDay',
  'perpWeek',
  'perpMonth',
  'perpAllTime',
]

class PortfolioMetrics(TypedDict):
  accountValueHistory: list[tuple[int, str]]
  pnlHistory: list[tuple[int, str]]
  vlm: str
  """Volume."""

class VaultFollower(TypedDict):
  user: str
  vaultEquity: str
  pnl: str
  allTimePnl: str
  daysFollowing: int
  vaultEntryTime: int
  lockupUntil: int

class VaultRelationshipData(TypedDict):
  childAddresses: list[str]

class VaultRelationship(TypedDict):
  type: str
  data: VaultRelationshipData

class VaultDetailsResponse(TypedDict):
  name: str
  vaultAddress: str
  leader: str
  description: str
  portfolio: list[tuple[PortfolioPeriod, PortfolioMetrics]]
  apr: float
  followerState: object | None
  leaderFraction: float
  leaderCommission: int
  followers: list[VaultFollower]
  maxDistributable: float
  maxWithdrawable: float
  isClosed: bool
  relationship: VaultRelationship
  allowDeposits: bool
  alwaysCloseOnWithdraw: bool

adapter = pydantic.TypeAdapter(VaultDetailsResponse)

class VaultDetails(InfoMixin):
  async def vault_details(
    self, vault_address: str, *, user: str | None = None
  ) -> VaultDetailsResponse:
    """Return details for a vault.

    - `vault_address`: Vault address.
    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-details-for-a-vault)
    """
    params: dict[str, object] = {
      'type': 'vaultDetails',
      'vaultAddress': vault_address,
    }
    if user is not None:
      params['user'] = user
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
