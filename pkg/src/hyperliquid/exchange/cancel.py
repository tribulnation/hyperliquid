from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class Cancel(TypedDict):
  a: int
  """Asset index."""
  o: int
  """Order id."""

class CancelError(TypedDict):
  error: str

CancelStatus = Literal['success'] | CancelError

class CancelData(TypedDict):
  statuses: list[CancelStatus]

class CancelResponse(TypedDict):
  type: Literal['cancel']
  data: CancelData

adapter = pydantic.TypeAdapter(ExchangeResponse[CancelResponse])

class CancelOrders(ExchangeMixin):
  async def cancel(
    self, *cancels: Cancel,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[CancelResponse]:
    """Cancel one or more orders.

    - `cancels`: Cancel wire objects with asset + order id.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#cancel-order-s)
    """
    action = {
      'type': 'cancel',
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
