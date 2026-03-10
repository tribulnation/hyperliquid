from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class SpotAssetInfo(TypedDict):
  name: str
  """Asset name, e.g. "PURR/USDC"."""
  tokens: list[int]
  """Token indices that form the pair."""
  index: int
  """Spot pair index used in spot coin IDs (e.g. @107)."""
  isCanonical: bool

class EVMContract(TypedDict):
  address: str
  """EVM token contract address."""
  evm_extra_wei_decimals: int
  """Extra wei decimals beyond standard 18."""

class SpotTokenInfo(TypedDict):
  name: str
  """Token symbol, e.g. HYPE."""
  szDecimals: int
  """Size decimals used for quantities."""
  weiDecimals: int
  """Wei decimals used for on-chain units."""
  index: int
  """Token index used in spot metadata and asset IDs."""
  tokenId: str
  """Token identifier string."""
  isCanonical: bool
  evmContract: EVMContract | None
  fullName: str | None

class SpotMetaResponse(TypedDict):
  universe: list[SpotAssetInfo]
  """Spot assets/pairs metadata."""
  tokens: list[SpotTokenInfo]
  """Spot token metadata."""

adapter = pydantic.TypeAdapter(SpotMetaResponse)

class SpotMeta(InfoMixin):
  """Info client mixin for the spotMeta method."""

  async def spot_meta(self) -> SpotMetaResponse:
    """Return spot universe and token metadata.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot)
    """
    r = await self.request({'type': 'spotMeta'})
    return adapter.validate_python(r) if self.validate else r
