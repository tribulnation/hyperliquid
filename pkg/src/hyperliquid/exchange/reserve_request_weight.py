from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class ReserveRequestWeightAction(TypedDict):
  type: Literal['reserveRequestWeight']
  weight: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ReserveRequestWeight(ExchangeMixin):
  async def reserve_request_weight(
    self, *, weight: int,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Reserve additional actions.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#reserve-additional-actions)
    """
    action: ReserveRequestWeightAction = {
      'type': 'reserveRequestWeight',
      'weight': weight,
    }
    ts = timestamp.now()
    sig = sign_l1_action(
      action,
      wallet=self.wallet,
      nonce=ts,
      mainnet=self.mainnet,
      vault_address=None,
      expires_after=expires_after,
    )
    result = await self.client.request({
      'action': action,
      'nonce': ts,
      'signature': sig,
      'vaultAddress': None,
      'expiresAfter': expires_after,
    })
    return adapter.validate_python(result) if self.validate else result
