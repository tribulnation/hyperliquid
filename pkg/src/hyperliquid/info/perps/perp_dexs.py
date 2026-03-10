from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpDex(TypedDict):
  name: str
  fullName: str
  deployer: str
  oracleUpdater: str | None
  feeRecipient: str | None
  assetToStreamingOiCap: list[tuple[str, str]]
  assetToFundingMultiplier: list[tuple[str, str]]

adapter = pydantic.TypeAdapter(list[PerpDex|None])

class PerpDexs(InfoMixin):
  async def perp_dexs(self) -> list[PerpDex|None]:
    """Return all perp dexes.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-all-perpetual-dexs)
    """
    r = await self.request({'type': 'perpDexs'})
    return adapter.validate_python(r) if self.validate else r
