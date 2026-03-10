from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class MarginSummary(TypedDict):
  accountValue: float
  totalNtlPos: float
  totalRawUsd: float
  totalMarginUsed: float

class AssetPosition(TypedDict):
  type: Literal['oneWay']
  position: dict[str, object]

class ClearinghouseStateData(TypedDict):
  assetPositions: list[AssetPosition]
  marginSummary: MarginSummary
  crossMarginSummary: MarginSummary
  crossMaintenanceMarginUsed: float
  withdrawable: float

class ClearinghouseStateParams(TypedDict):
  user: str
  dex: str

adapter = pydantic.TypeAdapter(ClearinghouseStateData)

class ClearinghouseState(StreamsMixin):
  async def clearinghouse_state(self, user: str, dex: str):
    """Stream clearinghouse state for a user.

    - `user`: Account address.
    - `dex`: Perp dex name.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('clearinghouseState', {'user': user, 'dex': dex})
    def mapper(msg) -> ClearinghouseStateData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
