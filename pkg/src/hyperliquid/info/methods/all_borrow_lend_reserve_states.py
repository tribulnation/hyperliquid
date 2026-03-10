from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.info.core import InfoMixin

class BorrowLendReserveState(TypedDict):
  borrowYearlyRate: str
  supplyYearlyRate: str
  balance: str
  utilization: str
  oraclePx: str
  ltv: str
  totalSupplied: str
  totalBorrowed: str

AllBorrowLendReserveStatesResponse = list[tuple[int, BorrowLendReserveState]]

adapter = pydantic.TypeAdapter(AllBorrowLendReserveStatesResponse)

class AllBorrowLendReserveStates(InfoMixin):
  async def all_borrow_lend_reserve_states(self) -> AllBorrowLendReserveStatesResponse:
    """Return all borrow/lend reserve states.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-all-borrow-lend-reserve-states)
    """
    r = await self.request({'type': 'allBorrowLendReserveStates'})
    return adapter.validate_python(r) if self.validate else r
