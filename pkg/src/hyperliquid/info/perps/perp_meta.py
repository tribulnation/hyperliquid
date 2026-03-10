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

class PerpMetaResponse(TypedDict):
  universe: list[PerpAssetInfo]
  marginTables: list[tuple[int, MarginTable]]

adapter = pydantic.TypeAdapter(PerpMetaResponse)

class PerpMeta(InfoMixin):
  async def perp_meta(self, dex: str | None = None) -> PerpMetaResponse:
    """Return perpetuals metadata (universe and margin tables).

    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-perpetuals-metadata-universe-and-margin-tables)
    """
    params: dict[str, object] = {'type': 'meta'}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
