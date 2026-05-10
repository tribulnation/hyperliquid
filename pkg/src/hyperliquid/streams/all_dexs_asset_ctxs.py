from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class AllDexsAssetCtx(TypedDict):
  funding: str
  openInterest: str
  prevDayPx: str
  dayNtlVlm: str
  premium: str | None
  oraclePx: str
  markPx: str
  midPx: str | None
  impactPxs: list[str] | None
  dayBaseVlm: str

class AllDexsAssetCtxSummary(TypedDict):
  markPx: str

class AllDexsAssetCtxItem(TypedDict):
  coin: str
  ctx: AllDexsAssetCtx | AllDexsAssetCtxSummary

class AllDexsAssetCtxGroup(TypedDict):
  dex: str
  ctxs: list[AllDexsAssetCtxItem]

class AllDexsAssetCtxTupleData(TypedDict):
  ctxs: list[tuple[str, list[AllDexsAssetCtx]]]

AllDexsAssetCtxsData = list[AllDexsAssetCtxGroup] | AllDexsAssetCtxTupleData

adapter = pydantic.TypeAdapter(AllDexsAssetCtxsData)

class AllDexsAssetCtxs(StreamsMixin):
  async def all_dexs_asset_ctxs(self, *, validate: bool | None = None):
    """Stream asset contexts for all perp dexs.

    Args:
      validate: Override response validation for this call. When omitted,
        the client-level validation setting is used.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions#subscriptions)
    """
    should_validate = self.validate if validate is None else validate
    stream = await self.subscribe('allDexsAssetCtxs')
    def mapper(msg) -> AllDexsAssetCtxsData:
      return adapter.validate_python(msg) if should_validate else msg
    return stream.map(mapper)
