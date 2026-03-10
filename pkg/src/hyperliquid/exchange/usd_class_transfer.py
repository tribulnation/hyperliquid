from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class UsdClassTransferAction(TypedDict):
  type: Literal['usdClassTransfer']
  signatureChainId: str
  amount: str
  toPerp: bool
  nonce: int
  subaccount: NotRequired[str]

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class UsdClassTransfer(ExchangeMixin):
  async def usd_class_transfer(
    self, *, amount: str, to_perp: bool,
    signature_chain_id: str,
    subaccount: str | None = None,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Transfer USDC between spot and perp accounts.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#transfer-from-spot-account-to-perp-account-and-vice-versa)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: UsdClassTransferAction = {
      'type': 'usdClassTransfer',
      'signatureChainId': signature_chain_id,
      'amount': amount,
      'toPerp': to_perp,
      'nonce': ts,
    }
    if subaccount is not None:
      action['subaccount'] = subaccount
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'amount', 'type': 'string'},
        {'name': 'toPerp', 'type': 'bool'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:UsdClassTransfer',
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
