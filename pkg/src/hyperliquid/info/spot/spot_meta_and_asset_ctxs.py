from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin
from .spot_meta import SpotMetaResponse

class SpotAssetCtx(TypedDict):
  dayNtlVlm: str
  markPx: str
  midPx: str | None
  prevDayPx: str
  circulatingSupply: NotRequired[str]
  coin: NotRequired[str]

SpotMetaAndAssetCtxsResponse = tuple[SpotMetaResponse, list[SpotAssetCtx]]

adapter = pydantic.TypeAdapter(SpotMetaAndAssetCtxsResponse)

class SpotMetaAndAssetCtxs(InfoMixin):
  async def spot_meta_and_asset_ctxs(self) -> SpotMetaAndAssetCtxsResponse:
    """Return spot metadata and asset contexts.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-spot-asset-contexts)
    """
    r = await self.request({'type': 'spotMetaAndAssetCtxs'})
    return adapter.validate_python(r) if self.validate else r
