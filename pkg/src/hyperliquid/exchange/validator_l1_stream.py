from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class ValidatorL1StreamAction(TypedDict):
  type: Literal['validatorL1Stream']
  riskFreeRate: str

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ValidatorL1Stream(ExchangeMixin):
  async def validator_l1_stream(self, risk_free_rate: str) -> ExchangeResponse[DefaultResponse]:
    """Vote on risk-free rate for aligned quote asset.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#validator-vote-on-risk-free-rate-for-aligned-quote-asset)
    """
    action: ValidatorL1StreamAction = {
      'type': 'validatorL1Stream',
      'riskFreeRate': risk_free_rate,
    }
    ts = timestamp.now()
    sig = sign_l1_action(
      action,
      wallet=self.wallet,
      nonce=ts,
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
