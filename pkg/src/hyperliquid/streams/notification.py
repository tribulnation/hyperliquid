from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class NotificationData(TypedDict):
  notification: str

class NotificationParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(NotificationData)

class Notification(StreamsMixin):
  async def notification(self, user: str):
    """Stream notifications for a user.

    - `user`: User address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('notification', {'user': user})
    def mapper(msg) -> NotificationData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
