from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

PortfolioPeriod = Literal[
  'day',
  'week',
  'month',
  'allTime',
  'perpDay',
  'perpWeek',
  'perpMonth',
  'perpAllTime',
]

class PortfolioMetrics(TypedDict):
  accountValueHistory: list[tuple[int, str]]
  pnlHistory: list[tuple[int, str]]
  vlm: str
  """Volume."""

UserPortfolioResponse = list[tuple[PortfolioPeriod, PortfolioMetrics]]

adapter = pydantic.TypeAdapter(UserPortfolioResponse)

class UserPortfolio(InfoMixin):
  async def user_portfolio(self, user: str) -> UserPortfolioResponse:
    """Return a user's portfolio.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-portfolio)
    """
    r = await self.request({'type': 'portfolio', 'user': user})
    return adapter.validate_python(r) if self.validate else r
