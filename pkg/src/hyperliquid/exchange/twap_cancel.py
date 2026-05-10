from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class TwapCancelAction(TypedDict):
  type: Literal['twapCancel']
  a: int
  t: int

class TwapCancelError(TypedDict):
  error: str

TwapCancelStatus = Literal['success'] | TwapCancelError

class TwapCancelData(TypedDict):
  status: TwapCancelStatus

class TwapCancelResponse(TypedDict):
  type: Literal['twapCancel']
  data: TwapCancelData

adapter = pydantic.TypeAdapter(ExchangeResponse[TwapCancelResponse])

class TwapCancel(ExchangeMixin):
  async def twap_cancel(
    self, *, asset: int, twap_id: int,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[TwapCancelResponse]:
    """Cancel a TWAP order.

    Args:
      asset: Asset index.
      twap_id: TWAP order id.
      vault_address: Optional vault address for the signed action.
      expires_after: Optional expiration timestamp for the signed action.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#cancel-a-twap-order)
    """
    action: TwapCancelAction = {
      'type': 'twapCancel',
      'a': asset,
      't': twap_id,
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
