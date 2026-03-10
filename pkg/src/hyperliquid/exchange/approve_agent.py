from typing_extensions import Literal, NotRequired
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class ApproveAgentAction(TypedDict, total=False):
  type: Literal['approveAgent']
  signatureChainId: str
  agentAddress: str
  agentName: NotRequired[str]
  nonce: int

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class ApproveAgent(ExchangeMixin):
  async def approve_agent(
    self, *, agent_address: str,
    signature_chain_id: str,
    agent_name: str | None = None,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Approve an API wallet (agent).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#approve-an-api-wallet)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: ApproveAgentAction = {
      'type': 'approveAgent',
      'signatureChainId': signature_chain_id,
      'agentAddress': agent_address,
      'nonce': ts,
    }
    if agent_name is not None:
      action['agentName'] = agent_name
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'agentAddress', 'type': 'address'},
        {'name': 'agentName', 'type': 'string'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:ApproveAgent',
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
