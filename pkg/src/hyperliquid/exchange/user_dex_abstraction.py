from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class UserDexAbstractionAction(TypedDict):
  type: Literal['userDexAbstraction']
  signatureChainId: str
  user: str
  enabled: bool
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UserDexAbstraction(ExchangeMixin):
  async def user_dex_abstraction(
    self, *, user: str, enabled: bool,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Enable HIP-3 DEX abstraction (deprecated).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#enable-hip-3-dex-abstraction)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: UserDexAbstractionAction = {
      'type': 'userDexAbstraction',
      'signatureChainId': signature_chain_id,
      'user': user,
      'enabled': enabled,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'user', 'type': 'address'},
        {'name': 'enabled', 'type': 'bool'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:UserDexAbstraction',
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
