from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class L2BookLevel(TypedDict):
  px: str
  sz: str
  n: int

class L2BookData(TypedDict):
  coin: str
  levels: list[list[L2BookLevel]]
  time: int

class L2BookParams(TypedDict):
  coin: str
  nSigFigs: NotRequired[int]
  mantissa: NotRequired[int]

adapter = pydantic.TypeAdapter(L2BookData)

class L2Book(StreamsMixin):
  def l2_book(
    self, coin: str, *,
    n_sig_figs: int | None = None,
    mantissa: int | None = None
  ):
    """Stream L2 book updates.

    Args:
      coin: Asset symbol.
      n_sig_figs: Aggregate levels to significant figures.
      mantissa: Only allowed when `n_sig_figs` is 5.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions#subscription-messages)
    """
    return StreamManager(lambda: self._l2_book_impl(coin, n_sig_figs=n_sig_figs, mantissa=mantissa))

  async def _l2_book_impl(
    self, coin: str, *,
    n_sig_figs: int | None = None,
    mantissa: int | None = None
  ):
    params: L2BookParams = {'coin': coin}
    if n_sig_figs is not None:
      params['nSigFigs'] = n_sig_figs
    if mantissa is not None:
      params['mantissa'] = mantissa
    # `l2Book` is shared across all coins at the wire level (Hyperliquid
    # tags every message with the same "channel": "l2Book" regardless of
    # coin) -- use a coin-specific local channel key so concurrent
    # subscriptions for different coins don't collide in the local
    # subscription registry, and derive the same key from incoming
    # notifications so they route back to the right one.
    stream = await self.subscribe(
      f'l2Book:{coin.lower()}', params, request_channel='l2Book',
      message_key=lambda data: f'l2Book:{data["coin"].lower()}',
    )
    def mapper(msg) -> L2BookData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
