from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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
  def clearinghouse_state(self, user: str, dex: str):
    """Stream clearinghouse state for a user.

    Args:
      user: Account address.
      dex: Perp dex name.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._clearinghouse_state_impl(user, dex))

  async def _clearinghouse_state_impl(self, user: str, dex: str):
    stream = await self.subscribe('clearinghouseState', {'user': user, 'dex': dex})
    def mapper(msg) -> ClearinghouseStateData:
      data = msg.get('clearinghouseState', msg)
      return adapter.validate_python(data) if self.validate else data
    return stream.map(mapper)
