from typing_extensions import Literal, AsyncIterable, TypeVar, Generic, Any, Callable, Awaitable
from hyperliquid.core import TypedDict
from abc import abstractmethod
from dataclasses import dataclass, field, replace
from collections import defaultdict
import inspect
import asyncio

from .base import RpcSocketClient

M = TypeVar('M', default=Any)
R = TypeVar('R', default=Any)
S = TypeVar('S', default=Any)
T = TypeVar('T', default=Any)
SP = TypeVar('SP', default=Any)
SR = TypeVar('SR', default=Any)
UR = TypeVar('UR', default=Any)

class Response(TypedDict, Generic[R]):
  kind: Literal['response']
  id: int | str
  response: R

class Subscription(TypedDict, Generic[S]):
  kind: Literal['subscription']
  channel: str
  data: S

Message = Response[R] | Subscription[S]

@dataclass
class Stream(AsyncIterable[S], Generic[S, SR, UR]):
  reply: SR
  stream: AsyncIterable[S]
  unsubscribe: Callable[[], Awaitable[UR]]

  def __aiter__(self):
    return self.stream.__aiter__()

  async def on(self, listener: Callable[[S], Awaitable[None] | None]):
    async for msg in self.stream:
      out = listener(msg)
      if inspect.isawaitable(out):
        await out

  def map(self, f: Callable[[S], T]) -> 'Stream[T, SR, UR]':
    async def stream() -> AsyncIterable[T]:
      async for msg in self.stream:
        yield f(msg)
    return replace(self, stream=stream()) # type: ignore

  def filter(self, f: Callable[[S], bool]) -> 'Stream[S, SR, UR]':
    async def stream() -> AsyncIterable[S]:
      async for msg in self.stream:
        if f(msg):
          yield msg
    return replace(self, stream=stream()) # type: ignore


@dataclass
class MultiplexStreamsRPCSocketClient(RpcSocketClient[M, R], Generic[M, R, S, SR, UR]):
  """Multiplexed request/response and streams socket client. It uses IDs to identify requests and responses. It also supports subscription to multiple channels."""
  replies: dict[int|str, asyncio.Future[R]] = field(default_factory=dict, init=False, repr=False)
  counter: int = field(default=0, init=False, repr=False)
  subscribers: dict[str, list[asyncio.Queue[S]]] = field(default_factory=lambda: defaultdict(list), init=False, repr=False)

  async def rpc_request(self, msg: M) -> R:
    id = self.counter
    self.counter += 1
    self.replies[id] = asyncio.Future()
    await self.rpc_send(id, msg)
    res = await self.wait_with_listener(self.replies[id])
    del self.replies[id]
    return res
    
  @abstractmethod
  async def req_subscription(self, channel: str, params: SP | None = None) -> SR:
    ...

  @abstractmethod
  async def req_unsubscription(self, channel: str, params: SP | None = None) -> UR:
    ...

  @abstractmethod
  def parse_msg(self, msg: str | bytes) -> Message[R, S] | None:
    ...

  def on_msg(self, msg: str | bytes):
    if (res := self.parse_msg(msg)) is not None:
      if res['kind'] == 'response':
        self.replies[res['id']].set_result(res['response']) # type: ignore
      else:
        for q in self.subscribers[res['channel']]:
          q.put_nowait(res['data']) # type: ignore

  @abstractmethod
  async def rpc_send(self, id: int, msg: M):
    ...

  async def subscribe(self, channel: str, params: SP | None = None) -> Stream[S, SR, UR]:
    q = asyncio.Queue()
    self.subscribers[channel].append(q)
    reply = await self.req_subscription(channel, params)

    async def stream() -> AsyncIterable[S]:
      while True:
        yield await self.wait_with_listener(asyncio.create_task(q.get()))

    async def unsubscribe() -> UR:
      del self.subscribers[channel]
      return await self.req_unsubscription(channel, params)

    return Stream(reply, stream(), unsubscribe)
