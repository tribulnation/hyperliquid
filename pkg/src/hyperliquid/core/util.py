import time
from datetime import datetime

HYPERLIQUID_MAINNET = 'api.hyperliquid.xyz'
HYPERLIQUID_TESTNET = 'api.hyperliquid-testnet.xyz'

class timestamp:
  @staticmethod
  def parse(time: int | str) -> datetime:
    return datetime.fromtimestamp(int(time)/1e3)
  
  @staticmethod
  def dump(dt: datetime) -> int:
    return int(1e3*dt.timestamp())
  
  @staticmethod
  def now() -> int:
    return int(time.time() * 1e3)