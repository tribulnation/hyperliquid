from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class PerpAnnotationResponse(TypedDict):
  category: str
  description: str

adapter = pydantic.TypeAdapter(PerpAnnotationResponse | None)

class PerpAnnotation(InfoMixin):
  async def perp_annotation(self, coin: str) -> PerpAnnotationResponse | None:
    """Return perp annotation for a coin.

    Args:
      coin: Coin name, e.g. "BTC".

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#retrieve-perp-annotation)
    """
    r = await self.request({'type': 'perpAnnotation', 'coin': coin})
    return adapter.validate_python(r) if self.validate else r
