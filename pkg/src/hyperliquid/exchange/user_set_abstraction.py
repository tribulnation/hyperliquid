from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

Abstraction = Literal['disabled', 'unifiedAccount', 'portfolioMargin']

class UserSetAbstractionAction(TypedDict):
  type: Literal['userSetAbstraction']
  signatureChainId: str
  user: str
  abstraction: Abstraction
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UserSetAbstraction(ExchangeMixin):
  async def user_set_abstraction(
    self, *, user: str, abstraction: Abstraction,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Set user abstraction.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#set-user-abstraction)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: UserSetAbstractionAction = {
      'type': 'userSetAbstraction',
      'signatureChainId': signature_chain_id,
      'user': user,
      'abstraction': abstraction,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'user', 'type': 'address'},
        {'name': 'abstraction', 'type': 'string'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:UserSetAbstraction',
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
