from typing_extensions import NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

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
  async def l2_book(
    self, coin: str, *,
    n_sig_figs: int | None = None,
    mantissa: int | None = None
  ):
    """Stream L2 book updates.

    - `coin`: Asset symbol.
    - `n_sig_figs`: Aggregate levels to significant figures.
    - `mantissa`: Only allowed when `n_sig_figs` is 5.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    params: L2BookParams = {'coin': coin}
    if n_sig_figs is not None:
      params['nSigFigs'] = n_sig_figs
    if mantissa is not None:
      params['mantissa'] = mantissa
    stream = await self.subscribe('l2Book', params)
    coin_l = coin.lower()
    stream = stream.filter(lambda msg: msg.get('coin', '').lower() == coin_l)
    def mapper(msg) -> L2BookData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
