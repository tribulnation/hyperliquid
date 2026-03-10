from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class SpotPairDeployAuctionStatusResponse(TypedDict):
  startTimeSeconds: int
  durationSeconds: int
  startGas: str
  currentGas: str | None
  endGas: str | None

adapter = pydantic.TypeAdapter(SpotPairDeployAuctionStatusResponse)

class SpotPairDeployAuctionStatus(InfoMixin):
  async def spot_pair_deploy_auction_status(self) -> SpotPairDeployAuctionStatusResponse:
    """Return spot pair deploy auction status.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-information-about-the-spot-pair-deploy-auction)
    """
    r = await self.request({'type': 'spotPairDeployAuctionStatus'})
    return adapter.validate_python(r) if self.validate else r
