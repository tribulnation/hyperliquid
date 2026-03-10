from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class TokenGenesis(TypedDict):
  userBalances: list[tuple[str, str]]
  existingTokenBalances: list[tuple[int, str]]

class TokenDetailsResponse(TypedDict):
  name: str
  maxSupply: str
  totalSupply: str
  circulatingSupply: str
  szDecimals: int
  weiDecimals: int
  midPx: str
  markPx: str
  prevDayPx: str
  genesis: TokenGenesis
  deployer: str | None
  deployGas: str
  deployTime: str
  seededUsdc: str
  nonCirculatingUserBalances: list[tuple[str, str]]
  futureEmissions: str

adapter = pydantic.TypeAdapter(TokenDetailsResponse)

class TokenDetails(InfoMixin):
  async def token_details(self, token_id: str) -> TokenDetailsResponse:
    """Return token details.

    - `token_id`: Onchain token id.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-information-about-a-token)
    """
    r = await self.request({'type': 'tokenDetails', 'tokenId': token_id})
    return adapter.validate_python(r) if self.validate else r
