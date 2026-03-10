from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PredictedFunding(TypedDict):
  fundingRate: str
  nextFundingTime: int

PredictedFundingsResponse = list[tuple[str, list[tuple[str, PredictedFunding]]]]

adapter = pydantic.TypeAdapter(PredictedFundingsResponse)

class PredictedFundings(InfoMixin):
  async def predicted_fundings(self) -> PredictedFundingsResponse:
    """Return predicted funding rates for different venues.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-predicted-funding-rates-for-different-venues)
    """
    r = await self.request({'type': 'predictedFundings'})
    return adapter.validate_python(r) if self.validate else r
