from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class UpdateIsolatedMarginAction(TypedDict):
  type: Literal['updateIsolatedMargin']
  asset: int
  isBuy: bool
  ntli: int

class TopUpIsolatedOnlyMarginAction(TypedDict):
  type: Literal['topUpIsolatedOnlyMargin']
  asset: int
  leverage: str

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UpdateIsolatedMargin(ExchangeMixin):
  async def update_isolated_margin(
    self, *, asset: int, is_buy: bool, ntli: int,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Add or remove margin from an isolated position.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#update-isolated-margin)
    """
    action: UpdateIsolatedMarginAction = {
      'type': 'updateIsolatedMargin',
      'asset': asset,
      'isBuy': is_buy,
      'ntli': ntli,
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

  async def top_up_isolated_only_margin(
    self, *, asset: int, leverage: str,
    vault_address: str | None = None,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Target leverage for isolated margin with an alternate action.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#update-isolated-margin)
    """
    action: TopUpIsolatedOnlyMarginAction = {
      'type': 'topUpIsolatedOnlyMargin',
      'asset': asset,
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
