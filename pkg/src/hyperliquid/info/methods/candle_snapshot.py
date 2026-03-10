from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class Candle(TypedDict):
  T: int
  """Timestamp of the end of the candle."""
  c: str
  """Closing price of the candle."""
  h: str
  """Highest price reached during the candle."""
  i: str
  """Time interval of the candle."""
  l: str
  """Lowest price reached during the candle."""
  n: int
  """Number of trades that occurred during the candle."""
  o: str
  """Opening price of the candle."""
  s: str
  """Asset being queried."""
  t: int
  """Timestamp of the beginning of the candle."""
  v: str
  """Volume traded during the candle."""

CandleSnapshotResponse = list[Candle]

adapter = pydantic.TypeAdapter(CandleSnapshotResponse)

class CandleSnapshot(InfoMixin):
  async def candle_snapshot(
    self, *, coin: str, interval: str,
    start_time: int, end_time: int
  ) -> CandleSnapshotResponse:
    """Return a candle snapshot.

    - `coin`: Asset being queried.
    - `interval`: Time interval of the candles.
    - `start_time`: Timestamp of the first candle in the snapshot (epoch ms).
    - `end_time`: Timestamp of the last candle in the snapshot (epoch ms).

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#candle-snapshot)
    """
    r = await self.request({
      'type': 'candleSnapshot',
      'req': {
        'coin': coin,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
      },
    })
    return adapter.validate_python(r) if self.validate else r
