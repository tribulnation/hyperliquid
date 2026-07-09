from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

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
  def active_asset_ctx(self, coin: str):
    """Stream active asset context.

    Args:
      coin: Asset symbol.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._active_asset_ctx_impl(coin))

  async def _active_asset_ctx_impl(self, coin: str):
    coin_l = coin.lower()
    # See `l2_book.py` -- `activeAssetCtx` messages are tagged the same way
    # regardless of coin, so use a coin-specific local channel key.
    stream = await self.subscribe(
      f'activeAssetCtx:{coin_l}', {'coin': coin}, request_channel='activeAssetCtx',
      message_key=lambda data: f'activeAssetCtx:{data["coin"].lower()}',
    )
    stream = stream.filter(lambda msg: msg.get('coin', '').lower() == coin_l)
    def mapper(msg) -> ActiveAssetCtxData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
