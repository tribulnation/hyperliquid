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

PerpMetaAndAssetCtxsResponse = tuple[PerpMeta, list[PerpAssetCtx]]

adapter = pydantic.TypeAdapter(PerpMetaAndAssetCtxsResponse)

class PerpMetaAndAssetCtxs(InfoMixin):
  async def perp_meta_and_asset_ctxs(
    self, dex: str | None = None
  ) -> PerpMetaAndAssetCtxsResponse:
    """Return perpetuals metadata and asset contexts.

    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-perpetuals-asset-contexts-includes-mark-price-current-funding-open-interest-etc)
    """
    params: dict[str, object] = {'type': 'metaAndAssetCtxs'}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
