from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class SpotTokenSpec(TypedDict):
  name: str
  szDecimals: int
  weiDecimals: int

class SpotDeployStateEntry(TypedDict):
  token: int
  spec: SpotTokenSpec
  fullName: str
  spots: list[int]
  maxSupply: int
  hyperliquidityGenesisBalance: str
  totalGenesisBalanceWei: str
  userGenesisBalances: list[tuple[str, str]]
  existingTokenGenesisBalances: list[tuple[int, str]]

class GasAuction(TypedDict):
  startTimeSeconds: int
  durationSeconds: int
  startGas: str
  currentGas: str | None
  endGas: str | None

class SpotDeployStateResponse(TypedDict):
  states: list[SpotDeployStateEntry]
  gasAuction: GasAuction

adapter = pydantic.TypeAdapter(SpotDeployStateResponse)

class SpotDeployState(InfoMixin):
  async def spot_deploy_state(self, user: str) -> SpotDeployStateResponse:
    """Return spot deploy auction status.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-information-about-the-spot-deploy-auction)
    """
    r = await self.request({'type': 'spotDeployState', 'user': user})
    return adapter.validate_python(r) if self.validate else r
