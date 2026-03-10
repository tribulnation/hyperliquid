from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class CancelByCloid(TypedDict):
  asset: int
  """Asset index."""
  cloid: str
  """Client order id (16-byte hex string)."""

class CancelError(TypedDict):
  error: str

CancelStatus = Literal['success'] | CancelError

class CancelData(TypedDict):
  statuses: list[CancelStatus]

class CancelByCloidResponse(TypedDict):
  type: Literal['cancelByCloid']
  data: CancelData

adapter = pydantic.TypeAdapter(ExchangeResponse[CancelByCloidResponse])

class CancelByCloidOrders(ExchangeMixin):
  async def cancel_by_cloid(
    self, *cancels: CancelByCloid,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[CancelByCloidResponse]:
    """Cancel one or more orders by cloid.

    - `cancels`: Cancel wire objects with asset + cloid.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#cancel-order-s-by-cloid)
    """
    action = {
      'type': 'cancelByCloid',
      'cancels': cancels,
    }
    ts = timestamp.now()
    sig = sign_l1_action(
      action,
      wallet=self.wallet,
      nonce=ts,
      mainnet=self.mainnet,
      vault_address=vault_address,
      expires_after=expires_after,
    )
    result = await self.client.request({
      'action': action,
      'nonce': ts,
      'signature': sig,
      'vaultAddress': vault_address,
      'expiresAfter': expires_after,
    })
    return adapter.validate_python(result) if self.validate else result
