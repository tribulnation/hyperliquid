from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class ApproveBuilderFeeAction(TypedDict):
  type: Literal['approveBuilderFee']
  signatureChainId: str
  maxFeeRate: str
  builder: str
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ApproveBuilderFee(ExchangeMixin):
  async def approve_builder_fee(
    self, *, max_fee_rate: str, builder: str,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Approve a maximum builder fee rate.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#approve-a-builder-fee)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: ApproveBuilderFeeAction = {
      'type': 'approveBuilderFee',
      'signatureChainId': signature_chain_id,
      'maxFeeRate': max_fee_rate,
      'builder': builder,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'maxFeeRate', 'type': 'string'},
        {'name': 'builder', 'type': 'address'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:ApproveBuilderFee',
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
