import pydantic

from hyperliquid.info.core import InfoMixin

AllMidsResponse = dict[str, str]

adapter = pydantic.TypeAdapter(AllMidsResponse)

class AllMids(InfoMixin):
  async def all_mids(self, dex: str | None = None) -> AllMidsResponse:
    """Return mids for all coins.

    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-mids-for-all-coins)
    """
    params = {'type': 'allMids'}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
