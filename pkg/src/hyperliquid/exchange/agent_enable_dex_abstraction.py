from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_l1_action

class AgentEnableDexAbstractionAction(TypedDict):
  type: Literal['agentEnableDexAbstraction']

class DefaultResponse(TypedDict):
  type: Literal['default']

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class AgentEnableDexAbstraction(ExchangeMixin):
  async def agent_enable_dex_abstraction(self) -> ExchangeResponse[DefaultResponse]:
    """Enable HIP-3 DEX abstraction (agent, deprecated).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#enable-hip-3-dex-abstraction-agent)
    """
    action: AgentEnableDexAbstractionAction = {'type': 'agentEnableDexAbstraction'}
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
