from typing_extensions import Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.core import timestamp
from hyperliquid.exchange.core import ExchangeMixin, ExchangeResponse, sign_user_signed_action

class SendToEvmWithDataAction(TypedDict):
  type: Literal['sendToEvmWithData']
  signatureChainId: str
  token: str
  amount: str
  sourceDex: str
  destinationRecipient: str
  addressEncoding: Literal['hex', 'base58']
  destinationChainId: int
  gasLimit: int
  data: str
  nonce: int

class DefaultResponse(TypedDict):
  type: str

adapter = pydantic.TypeAdapter(ExchangeResponse[DefaultResponse])

class SendToEvmWithData(ExchangeMixin):
  async def send_to_evm_with_data(
    self, *, token: str, amount: str, source_dex: str,
    destination_recipient: str, address_encoding: Literal['hex', 'base58'],
    destination_chain_id: int, gas_limit: int, data: str,
    signature_chain_id: str,
    nonce: int | None = None,
  ) -> ExchangeResponse[DefaultResponse]:
    """Send to EVM with data payload.

    Args:
      token: Token symbol or token id to send.
      amount: Decimal amount string.
      source_dex: Source DEX name. Use an empty string for the main DEX.
      destination_recipient: Recipient on the destination EVM chain.
      address_encoding: Encoding used for the destination recipient.
      destination_chain_id: Destination EVM chain id.
      gas_limit: Gas limit for the destination call.
      data: Hex-encoded calldata.
      signature_chain_id: Chain id used for the user-signed action.
      nonce: Optional action nonce. Defaults to the current timestamp.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint#send-to-evm-with-data)
    """
    ts = timestamp.now() if nonce is None else nonce
    action: SendToEvmWithDataAction = {
      'type': 'sendToEvmWithData',
      'signatureChainId': signature_chain_id,
      'token': token,
      'amount': amount,
      'sourceDex': source_dex,
      'destinationRecipient': destination_recipient,
      'addressEncoding': address_encoding,
      'destinationChainId': destination_chain_id,
      'gasLimit': gas_limit,
      'data': data,
      'nonce': ts,
    }
    sig = sign_user_signed_action(
      action,
      wallet=self.wallet,
      payload_types=[
        {'name': 'hyperliquidChain', 'type': 'string'},
        {'name': 'token', 'type': 'string'},
        {'name': 'amount', 'type': 'string'},
        {'name': 'sourceDex', 'type': 'string'},
        {'name': 'destinationRecipient', 'type': 'string'},
        {'name': 'addressEncoding', 'type': 'string'},
        {'name': 'destinationChainId', 'type': 'uint64'},
        {'name': 'gasLimit', 'type': 'uint64'},
        {'name': 'data', 'type': 'bytes'},
        {'name': 'nonce', 'type': 'uint64'},
      ],
      primary_type='HyperliquidTransaction:SendToEvmWithData',
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
