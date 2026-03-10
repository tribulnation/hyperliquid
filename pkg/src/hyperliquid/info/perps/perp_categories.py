import pydantic
from hyperliquid.info.core import InfoMixin

PerpCategoriesResponse = list[tuple[str, str]]

adapter = pydantic.TypeAdapter(PerpCategoriesResponse)

class PerpCategories(InfoMixin):
  async def perp_categories(self) -> PerpCategoriesResponse:
    """Return perp categories.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-perp-categories)
    """
    r = await self.request({'type': 'perpCategories'})
    return adapter.validate_python(r) if self.validate else r
