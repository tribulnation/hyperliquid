from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core.exc import ApiError
from hyperliquid.info.core import InfoMixin

class L2BookLevel(TypedDict):
  px: str
  """Price level."""
  sz: str
  """Size at this price level."""
  n: int
  """Number of levels at this price."""

class L2BookResponse(TypedDict):
  coin: str
  time: int
  levels: list[list[L2BookLevel]]

adapter = pydantic.TypeAdapter(L2BookResponse)

class L2Book(InfoMixin):
  async def l2_book(
    self, coin: str, *,
    n_sig_figs: int | None = None,
    mantissa: int | None = None
  ) -> L2BookResponse:
    """Return an L2 book snapshot.

    - `coin`: from `spot_meta['universe'][idx]['name']` or `perp_meta['universe'][idx]['name']`. See the [docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/asset-ids) for full details.
    - `n_sig_figs`: Aggregate levels to significant figures.
    - `mantissa`: Only allowed when `n_sig_figs` is 5.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#l2-book-snapshot)
    """
    params: dict[str, object] = {'type': 'l2Book', 'coin': coin}
    if n_sig_figs is not None:
      params['nSigFigs'] = n_sig_figs
    if mantissa is not None:
      params['mantissa'] = mantissa
    r = await self.request(params)
    if r is None:
      raise ApiError(f'L2 book "{coin}" not found')
    return adapter.validate_python(r) if self.validate else r
