from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class VaultTransferAction(TypedDict):
  type: Literal['vaultTransfer']
  vaultAddress: str
  isDeposit: bool
  usd: float

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class VaultTransfer(ExchangeMixin):
  async def vault_transfer(
    self, *, vault_address: str, is_deposit: bool, usd: float,
    expires_after: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Deposit or withdraw from a vault.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#deposit-or-withdraw-from-a-vault)
    """
    action: VaultTransferAction = {
      'type': 'vaultTransfer',
      'vaultAddress': vault_address,
      'isDeposit': is_deposit,
      'usd': usd,
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
