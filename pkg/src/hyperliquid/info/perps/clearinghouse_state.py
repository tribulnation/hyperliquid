from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class CumFunding(TypedDict):
  allTime: str
  sinceChange: str
  sinceOpen: str

class LeverageCross(TypedDict):
  type: Literal['cross']
  value: int

class LeverageIsolated(TypedDict):
  type: Literal['isolated']
  value: int
  rawUsd: str

Leverage = LeverageCross | LeverageIsolated

class Position(TypedDict):
  coin: str
  cumFunding: CumFunding
  entryPx: str
  leverage: Leverage
  liquidationPx: str | None
  marginUsed: str
  maxLeverage: int
  positionValue: str
  returnOnEquity: str
  szi: str
  unrealizedPnl: str

class AssetPosition(TypedDict):
  position: Position
  type: str

class MarginSummary(TypedDict):
  accountValue: str
  totalMarginUsed: str
  totalNtlPos: str
  totalRawUsd: str

class ClearinghouseStateResponse(TypedDict):
  assetPositions: list[AssetPosition]
  crossMaintenanceMarginUsed: str
  crossMarginSummary: MarginSummary
  marginSummary: MarginSummary
  time: int
  withdrawable: str

adapter = pydantic.TypeAdapter(ClearinghouseStateResponse)

class ClearinghouseState(InfoMixin):
  async def clearinghouse_state(
    self, user: str, *, dex: str | None = None
  ) -> ClearinghouseStateResponse:
    """Return a user's perpetuals account summary.

    - `user`: Account address.
    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-users-perpetuals-account-summary)
    """
    params: dict[str, object] = {'type': 'clearinghouseState', 'user': user}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
