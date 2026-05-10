from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class AlignedQuoteTokenInfoResponse(TypedDict):
  isAligned: bool
  firstAlignedTime: int
  evmMintedSupply: str
  dailyAmountOwed: list[tuple[str, str]]
  predictedRate: str

adapter = pydantic.TypeAdapter(AlignedQuoteTokenInfoResponse | None)

class AlignedQuoteTokenInfo(InfoMixin):
  async def aligned_quote_token_info(
    self, token: int
  ) -> AlignedQuoteTokenInfoResponse | None:
    """Return aligned quote token status for a token index.

    Args:
      token: Token index.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-aligned-quote-token-status)
    """
    r = await self.request({'type': 'alignedQuoteTokenInfo', 'token': token})
    return adapter.validate_python(r) if self.validate else r
