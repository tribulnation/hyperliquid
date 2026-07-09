from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class AllMidsData(TypedDict):
  mids: dict[str, str]

class AllMidsParams(TypedDict, total=False):
  dex: str

adapter = pydantic.TypeAdapter(AllMidsData)

class AllMids(StreamsMixin):
  def all_mids(self, dex: str | None = None):
    """Stream mids for all coins.

    Args:
      dex: Perp dex name. Defaults to the empty string which represents the
        first perp dex.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._all_mids_impl(dex))

  async def _all_mids_impl(self, dex: str | None = None):
    params: AllMidsParams | None = None
    if dex is not None:
      params = {'dex': dex}
    stream = await self.subscribe('allMids', params)
    def mapper(msg) -> AllMidsData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
