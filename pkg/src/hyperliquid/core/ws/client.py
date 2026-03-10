from typing_extensions import Any, Literal, Union, Annotated, Mapping, TypeAlias, TypeGuard
from hyperliquid.core import TypedDict
from dataclasses import dataclass, field
import json
import logging
import websockets
from pydantic import TypeAdapter, Tag, Discriminator
import asyncio

from .multiplex_streams_rpc import MultiplexStreamsRPCSocketClient, Message
from ..exc import NetworkError, ApiError

class PostInfoPayload(TypedDict):
  type: str
  """Method being used"""
  data: Any
  """Actual reply you'd get from the HTTP API (yes this compulsive nesting is ridiculous)"""

class PostInfoResponse(TypedDict):
  type: Literal['info']
  payload: Any

class OtherPostResponse(TypedDict):
  type: Literal['action', 'error']
  payload: Any

PostResponse = PostInfoResponse | OtherPostResponse

class PostData(TypedDict):
  id: int
  response: PostResponse

class PostMessage(TypedDict):
  channel: Literal['post']
  data: PostData

class ErrorMessage(TypedDict):
  channel: Literal['error']
  data: Any

class SubscriptionResponseData(TypedDict):
  method: Literal['subscribe', 'unsubscribe']
  subscription: dict

class SubscriptionResponse(TypedDict):
  channel: Literal['subscriptionResponse']
  data: SubscriptionResponseData

class SubscriptionMessage(TypedDict):
  channel: str
  data: Any

def msg_discriminator(msg) -> Literal['post', 'subscription', 'subscriptionResponse', 'error']:
  if isinstance(msg, Mapping):
    if msg.get('channel') == 'post':
      return 'post'
    elif msg.get('channel') == 'subscriptionResponse':
      return 'subscriptionResponse'
    elif msg.get('channel') == 'error':
      return 'error'
  return 'subscription'

ServerMessage: TypeAlias = Annotated[
  Union[
    Annotated[PostMessage, Tag('post')],
    Annotated[SubscriptionMessage, Tag('subscription')],
    Annotated[SubscriptionResponse, Tag('subscriptionResponse')],
    Annotated[ErrorMessage, Tag('error')],
  ],
  Discriminator(msg_discriminator),
]
msg_adapter = TypeAdapter[PostMessage|SubscriptionMessage|SubscriptionResponse](ServerMessage)

def is_post_msg(msg: ServerMessage) -> TypeGuard[PostMessage]:
  return msg['channel'] == 'post'

def is_subscription_response(msg: ServerMessage) -> TypeGuard[SubscriptionResponse]:
  return msg['channel'] == 'subscriptionResponse'

def is_error_msg(msg: ServerMessage) -> TypeGuard[ErrorMessage]:
  return msg['channel'] == 'error'

class Request(TypedDict):
  type: Literal['info', 'action']
  payload: Any

logger = logging.getLogger('hyperliquid.core.ws')

@dataclass
class SocketClient(MultiplexStreamsRPCSocketClient[Any, Any, Any, SubscriptionResponseData, SubscriptionResponseData]):
  serial_messages: asyncio.Queue[SubscriptionResponse|ErrorMessage] = field(default_factory=asyncio.Queue, init=False, repr=False)

  async def req_subscription(self, channel: str, params=None):
    await self.send({
      'method': 'subscribe',
      'subscription': {
        'type': channel,
        **(params or {}),
      },
    })
    msg = await self.serial_messages.get()
    if is_subscription_response(msg):
      return msg['data']
    else:
      raise ApiError(msg['data'])

  async def req_unsubscription(self, channel: str, params=None):
    await self.send({
      'method': 'unsubscribe',
      'subscription': {
        'type': channel,
        **(params or {}),
      }
    })
    msg = await self.serial_messages.get()
    if is_subscription_response(msg):
      return msg['data']
    else:
      raise ApiError(msg['data'])

  async def rpc_send(self, id: int, msg):
    return await self.send({
      'method': 'post',
      'id': id,
      'request': msg,
    })
  
  async def send(self, msg):
    ws = await self.ws
    try:
      await ws.send(json.dumps(msg), text=True)
    except websockets.exceptions.WebSocketException as e:
      raise NetworkError(f'Error sending message: {msg}', type(e).__name__, *e.args) from e

  def parse_msg(self, msg: str | bytes) -> Message | None:
    obj = msg_adapter.validate_json(msg)
    if is_post_msg(obj):
      return {
        'kind': 'response',
        'id': obj['data']['id'],
        'response': obj['data']['response'],
      }
    elif is_subscription_response(obj) or is_error_msg(obj):
      self.serial_messages.put_nowait(obj)
    else:
      return {
        'kind': 'subscription',
        'channel': obj['channel'],
        'data': obj['data'],
      }

  async def request(self, request: Request) -> PostResponse:
    return await self.rpc_request(request)
    