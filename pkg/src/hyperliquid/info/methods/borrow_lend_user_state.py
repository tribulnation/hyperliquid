from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class BorrowLendValue(TypedDict):
  basis: str
  value: str

class BorrowLendTokenState(TypedDict):
  borrow: BorrowLendValue
  supply: BorrowLendValue

class BorrowLendUserStateResponse(TypedDict):
  tokenToState: list[tuple[int, BorrowLendTokenState]]
  health: str
  healthFactor: float | None

adapter = pydantic.TypeAdapter(BorrowLendUserStateResponse)

class BorrowLendUserState(InfoMixin):
  async def borrow_lend_user_state(
    self, user: str
  ) -> BorrowLendUserStateResponse:
    """Return borrow/lend user state.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-borrow-lend-user-state)
    """
    r = await self.request({'type': 'borrowLendUserState', 'user': user})
    return adapter.validate_python(r) if self.validate else r
