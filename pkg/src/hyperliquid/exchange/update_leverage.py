from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class UpdateLeverageAction(TypedDict):
  type: Literal['updateLeverage']
  asset: int
  isCross: bool
  leverage: int

class DefaultResponse(TypedDict):
  type: str

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UpdateLeverage(ExchangeMixin):
  async def update_leverage(
    self, *, asset: int, is_cross: bool, leverage: int,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Update cross or isolated leverage.

    Args:
      asset: Asset index.
      is_cross: Whether to use cross margin.
      leverage: Target leverage.
      vault_address: Optional vault address for the signed action.
      expires_after: Optional expiration timestamp for the signed action.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#update-leverage)
    """
    action: UpdateLeverageAction = {
      'type': 'updateLeverage',
      'asset': asset,
      'isCross': is_cross,
      'leverage': leverage,
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
