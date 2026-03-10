from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class UsdSendAction(TypedDict):
  type: Literal['usdSend']
  signatureChainId: str
  destination: str
  amount: str
  time: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UsdcTransfer(ExchangeMixin):
  async def usdc_transfer(
    self, *, destination: str, amount: str,
    signature_chain_id: str,
    time: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Core USDC transfer.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#core-usdc-transfer)
    """
    ts = timestamp.now()
    action: UsdSendAction = {
      'type': 'usdSend',
      'signatureChainId': signature_chain_id,
      'destination': destination,
      'amount': amount,
      'time': ts if time is None else time,
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
      primary_type='HyperliquidTransaction:UsdSend',
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
