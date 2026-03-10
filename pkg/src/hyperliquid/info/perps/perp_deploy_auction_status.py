from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpDeployAuctionStatusResponse(TypedDict):
  startTimeSeconds: int
  durationSeconds: int
  startGas: str
  currentGas: str | None
  endGas: str | None

adapter = pydantic.TypeAdapter(PerpDeployAuctionStatusResponse)

class PerpDeployAuctionStatus(InfoMixin):
  async def perp_deploy_auction_status(self) -> PerpDeployAuctionStatusResponse:
    """Return perp deploy auction status.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-information-about-the-perp-deploy-auction)
    """
    r = await self.request({'type': 'perpDeployAuctionStatus'})
    return adapter.validate_python(r) if self.validate else r
