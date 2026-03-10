from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

AgentAbstraction = Literal['i', 'u', 'p']

class AgentSetAbstractionAction(TypedDict):
  type: Literal['agentSetAbstraction']
  abstraction: AgentAbstraction

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class AgentSetAbstraction(ExchangeMixin):
  async def agent_set_abstraction(self, abstraction: AgentAbstraction) -> ExchangeResponse[DefaultResponse]:
    """Set user abstraction (agent).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#set-user-abstraction-agent)
    """
    action: AgentSetAbstractionAction = {
      'type': 'agentSetAbstraction',
      'abstraction': abstraction,
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
