from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class SendAssetAction(TypedDict):
  type: Literal['sendAsset']
  signatureChainId: str
  destination: str
  sourceDex: str
  destinationDex: str
  token: str
  amount: str
  fromSubAccount: str
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class SendAsset(ExchangeMixin):
  async def send_asset(
    self, *, destination: str, source_dex: str, destination_dex: str,
    token: str, amount: str, from_subaccount: str,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Send assets between DEXs, spot, users, or subaccounts.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#send-asset)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: SendAssetAction = {
      'type': 'sendAsset',
      'signatureChainId': signature_chain_id,
      'destination': destination,
      'sourceDex': source_dex,
      'destinationDex': destination_dex,
      'token': token,
      'amount': amount,
      'fromSubAccount': from_subaccount,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'destination', 'type': 'string'},
        {'name': 'sourceDex', 'type': 'string'},
        {'name': 'destinationDex', 'type': 'string'},
        {'name': 'token', 'type': 'string'},
        {'name': 'amount', 'type': 'string'},
        {'name': 'fromSubAccount', 'type': 'string'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:SendAsset',
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
