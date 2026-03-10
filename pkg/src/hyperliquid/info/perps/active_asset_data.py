from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class LeverageCross(TypedDict):
  type: Literal['cross']
  value: int

class LeverageIsolated(TypedDict):
  type: Literal['isolated']
  value: int
  rawUsd: str

Leverage = LeverageCross | LeverageIsolated

class ActiveAssetDataResponse(TypedDict):
  user: str
  coin: str
  leverage: Leverage
  maxTradeSzs: list[str]
  availableToTrade: list[str]
  markPx: str

adapter = pydantic.TypeAdapter(ActiveAssetDataResponse)

class ActiveAssetData(InfoMixin):
  async def active_asset_data(
    self, user: str, coin: str
  ) -> ActiveAssetDataResponse:
    """Return user's active asset data.

    - `user`: Account address.
    - `coin`: Coin, e.g. "ETH".

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-users-active-asset-data)
    """
    r = await self.request({'type': 'activeAssetData', 'user': user, 'coin': coin})
    return adapter.validate_python(r) if self.validate else r
