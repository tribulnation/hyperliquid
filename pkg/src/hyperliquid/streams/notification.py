from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class NotificationData(TypedDict):
  notification: str

class NotificationParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(NotificationData)

class Notification(StreamsMixin):
  def notification(self, user: str):
    """Stream notifications for a user.

    Args:
      user: User address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._notification_impl(user))

  async def _notification_impl(self, user: str):
    stream = await self.subscribe('notification', {'user': user})
    def mapper(msg) -> NotificationData:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
