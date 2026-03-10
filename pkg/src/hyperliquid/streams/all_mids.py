from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from hyperliquid.core.ws.multiplex_streams_rpc import Stream
from hyperliquid.core.ws.client import SubscriptionResponseData

class AllMidsData(TypedDict):
  mids: dict[str, str]

class AllMidsParams(TypedDict, total=False):
  dex: str

adapter = pydantic.TypeAdapter(AllMidsData)

class AllMids(StreamsMixin):
  async def all_mids(self, dex: str | None = None):
    """Stream mids for all coins.

    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    params: AllMidsParams | None = None
    if dex is not None:
      params = {'dex': dex}
    stream = await self.subscribe('allMids', params)
    def mapper(msg) -> AllMidsData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
