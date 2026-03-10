from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.info.core import InfoMixin

class BorrowLendReserveStateResponse(TypedDict):
  borrowYearlyRate: str
  supplyYearlyRate: str
  balance: str
  utilization: str
  oraclePx: str
  ltv: str
  totalSupplied: str
  totalBorrowed: str

adapter = pydantic.TypeAdapter(BorrowLendReserveStateResponse)

class BorrowLendReserveState(InfoMixin):
  async def borrow_lend_reserve_state(
    self, token: int
  ) -> BorrowLendReserveStateResponse:
    """Return borrow/lend reserve state for a token index.

    - `token`: Token index.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-borrow-lend-reserve-state)
    """
    r = await self.request({'type': 'borrowLendReserveState', 'token': token})
    return adapter.validate_python(r) if self.validate else r
