from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpDexStatusResponse(TypedDict):
  totalNetDeposit: str

adapter = pydantic.TypeAdapter(PerpDexStatusResponse)

class PerpDexStatus(InfoMixin):
  async def perp_dex_status(self, dex: str = '') -> PerpDexStatusResponse:
    """Return perp dex status.

    - `dex`: Perp dex name. The empty string represents the first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#get-perp-market-status)
    """
    r = await self.request({'type': 'perpDexStatus', 'dex': dex})
    return adapter.validate_python(r) if self.validate else r
