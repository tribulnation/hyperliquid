from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class AlignedQuoteTokenInfoResponse(TypedDict):
  isAligned: bool
  firstAlignedTime: int
  evmMintedSupply: str
  dailyAmountOwed: list[tuple[str, str]]
  predictedRate: str

adapter = pydantic.TypeAdapter(AlignedQuoteTokenInfoResponse)

class AlignedQuoteTokenInfo(InfoMixin):
  async def aligned_quote_token_info(
    self, token: int
  ) -> AlignedQuoteTokenInfoResponse:
    """Return aligned quote token status for a token index.

    - `token`: Token index.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-aligned-quote-token-status)
    """
    r = await self.request({'type': 'alignedQuoteTokenInfo', 'token': token})
    return adapter.validate_python(r) if self.validate else r
