from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class SpotBalance(TypedDict):
  coin: str
  token: int
  hold: str
  total: str
  entryNtl: str

class SpotClearinghouseStateResponse(TypedDict):
  balances: list[SpotBalance]

adapter = pydantic.TypeAdapter(SpotClearinghouseStateResponse)

class SpotClearinghouseState(InfoMixin):
  async def spot_clearinghouse_state(self, user: str) -> SpotClearinghouseStateResponse:
    """Return a user's spot token balances.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot#retrieve-a-users-token-balances)
    """
    r = await self.request({'type': 'spotClearinghouseState', 'user': user})
    return adapter.validate_python(r) if self.validate else r
