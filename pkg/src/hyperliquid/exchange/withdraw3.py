from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class Withdraw3Action(TypedDict):
  type: Literal['withdraw3']
  signatureChainId: str
  amount: str
  time: int
  destination: str

class DefaultResponse(TypedDict):
  type: str

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class Withdraw3(ExchangeMixin):
  async def withdraw3(
    self, *, amount: str, destination: str,
    signature_chain_id: str,
    time: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Initiate a withdrawal request.

    Args:
      amount: Decimal USDC amount string.
      destination: Destination address.
      signature_chain_id: Chain id used for the user-signed action.
      time: Optional action timestamp. Defaults to the current timestamp.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#initiate-a-withdrawal-request)
    """
    ts = timestamp.now()
    action: Withdraw3Action = {
      'type': 'withdraw3',
      'signatureChainId': signature_chain_id,
      'amount': amount,
      'time': ts if time is None else time,
      'destination': destination,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'destination', 'type': 'string'},
        {'name': 'amount', 'type': 'string'},
        {'name': 'time', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:Withdraw',
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
