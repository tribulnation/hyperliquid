import pydantic
from hyperliquid.info.core import InfoMixin

PerpsAtOpenInterestCapResponse = list[str]

adapter = pydantic.TypeAdapter(PerpsAtOpenInterestCapResponse)

class PerpsAtOpenInterestCap(InfoMixin):
  async def perps_at_open_interest_cap(
    self, dex: str | None = None
  ) -> PerpsAtOpenInterestCapResponse:
    """Return perps at open interest caps.

    - `dex`: Perp dex name. Defaults to the empty string which represents the
      first perp dex.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-perps-at-open-interest-caps)
    """
    params: dict[str, object] = {'type': 'perpsAtOpenInterestCap'}
    if dex is not None:
      params['dex'] = dex
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r
