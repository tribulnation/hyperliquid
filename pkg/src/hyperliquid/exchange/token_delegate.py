from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class TokenDelegateAction(TypedDict):
  type: Literal['tokenDelegate']
  signatureChainId: str
  validator: str
  isUndelegate: bool
  wei: int
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class TokenDelegate(ExchangeMixin):
  async def token_delegate(
    self, *, validator: str, is_undelegate: bool, wei: int,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Delegate or undelegate stake to a validator.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#delegate-or-undelegate-stake-from-validator)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: TokenDelegateAction = {
      'type': 'tokenDelegate',
      'signatureChainId': signature_chain_id,
      'validator': validator,
      'isUndelegate': is_undelegate,
      'wei': wei,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'validator', 'type': 'address'},
        {'name': 'wei', 'type': 'uint64'},
        {'name': 'isUndelegate', 'type': 'bool'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:TokenDelegate',
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
