from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpDexLimitsResponse(TypedDict):
  totalOiCap: str
  oiSzCapPerPerp: str
  maxTransferNtl: str
  coinToOiCap: list[tuple[str, str]]

adapter = pydantic.TypeAdapter(PerpDexLimitsResponse)

class PerpDexLimits(InfoMixin):
  async def perp_dex_limits(self, dex: str) -> PerpDexLimitsResponse:
    """Return builder-deployed perp market limits.

    - `dex`: Perp dex name (empty string not allowed).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-builder-deployed-perp-market-limits)
    """
    r = await self.request({'type': 'perpDexLimits', 'dex': dex})
    return adapter.validate_python(r) if self.validate else r
