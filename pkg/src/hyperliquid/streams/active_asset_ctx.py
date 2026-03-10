from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class PerpAssetCtx(TypedDict):
  funding: str
  openInterest: str
  prevDayPx: str
  dayNtlVlm: str
  premium: str
  oraclePx: str
  markPx: str
  midPx: NotRequired[str]
  impactPxs: NotRequired[tuple[str, str]]
  dayBaseVlm: str

class SpotAssetCtx(TypedDict):
  dayNtlVlm: str
  markPx: str
  midPx: NotRequired[str]
  prevDayPx: str
  circulatingSupply: str

class WsActiveAssetCtx(TypedDict):
  coin: str
  ctx: PerpAssetCtx

class WsActiveSpotAssetCtx(TypedDict):
  coin: str
  ctx: SpotAssetCtx

ActiveAssetCtxData = WsActiveAssetCtx | WsActiveSpotAssetCtx

class ActiveAssetCtxParams(TypedDict):
  coin: str

adapter = pydantic.TypeAdapter(ActiveAssetCtxData)

class ActiveAssetCtx(StreamsMixin):
  async def active_asset_ctx(self, coin: str):
    """Stream active asset context.

    - `coin`: Asset symbol.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('activeAssetCtx', {'coin': coin})
    coin_l = coin.lower()
    stream = stream.filter(lambda msg: msg.get('coin', '').lower() == coin_l)
    def mapper(msg) -> ActiveAssetCtxData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
