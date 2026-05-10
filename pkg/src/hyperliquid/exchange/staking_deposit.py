from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class CDepositAction(TypedDict):
  type: Literal['cDeposit']
  signatureChainId: str
  wei: int
  nonce: int

class DefaultResponse(TypedDict):
  type: str

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class StakingDeposit(ExchangeMixin):
  async def staking_deposit(
    self, *, wei: int,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Deposit native token into staking.

    Args:
      wei: Amount to deposit in wei.
      signature_chain_id: Chain id used for the user-signed action.
      nonce: Optional action nonce. Defaults to the current timestamp.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#deposit-into-staking)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: CDepositAction = {
      'type': 'cDeposit',
      'signatureChainId': signature_chain_id,
      'wei': wei,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'wei', 'type': 'uint64'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:Deposit',
      mainnet=self.mainnet,
    )
    result = await self.client.request({
      'action': action,
      'nonce': ts,
      'signature': sig,
      'vaultAddress': None,
      'expiresAfter': None,
    })
    return adapter.validate_python(result) if self.validate else result
