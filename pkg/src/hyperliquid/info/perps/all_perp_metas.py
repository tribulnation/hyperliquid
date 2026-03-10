from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpAssetInfo(TypedDict):
  name: str
  szDecimals: int
  maxLeverage: int
  marginTableId: NotRequired[int]
  onlyIsolated: NotRequired[bool]
  isDelisted: NotRequired[bool]
  marginMode: NotRequired[str]
  growthMode: NotRequired[str]
  lastGrowthModeChangeTime: NotRequired[str]

class MarginTier(TypedDict):
  lowerBound: str
  maxLeverage: int

class MarginTable(TypedDict):
  description: str
  marginTiers: list[MarginTier]

class PerpMeta(TypedDict):
  universe: list[PerpAssetInfo]
  marginTables: list[tuple[int, MarginTable]]
  collateralToken: int

class PerpAssetCtx(TypedDict):
  dayNtlVlm: str
  funding: str
  impactPxs: list[str] | None
  markPx: str | None
  midPx: str | None
  openInterest: str
  oraclePx: str
  premium: str | None
  prevDayPx: str
  dayBaseVlm: NotRequired[str]

AllPerpMetasResponse = list[tuple[PerpMeta, list[PerpAssetCtx]]]

adapter = pydantic.TypeAdapter(AllPerpMetasResponse)

class AllPerpMetas(InfoMixin):
  async def all_perp_metas(self) -> AllPerpMetasResponse:
    """Return all perpetuals metadata and asset contexts.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-all-perpetuals-metadata-universe-and-margin-tables)
    """
    r = await self.request({'type': 'allPerpMetas'})
    return adapter.validate_python(r) if self.validate else r
