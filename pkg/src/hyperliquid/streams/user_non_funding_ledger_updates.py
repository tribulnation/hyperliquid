from typing_extensions import NotRequired, Literal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin

class LiquidatedPosition(TypedDict):
  coin: str
  szi: float

class WsDeposit(TypedDict):
  type: Literal['deposit']
  usdc: float

class WsWithdraw(TypedDict):
  type: Literal['withdraw']
  usdc: float
  nonce: int
  fee: float

class WsInternalTransfer(TypedDict):
  type: Literal['internalTransfer']
  usdc: float
  user: str
  destination: str
  fee: float

class WsSubAccountTransfer(TypedDict):
  type: Literal['subAccountTransfer']
  usdc: float
  user: str
  destination: str

class WsLedgerLiquidation(TypedDict):
  type: Literal['liquidation']
  accountValue: float
  leverageType: Literal['Cross', 'Isolated']
  liquidatedPositions: list[LiquidatedPosition]

class WsVaultDelta(TypedDict):
  type: Literal['vaultCreate', 'vaultDeposit', 'vaultDistribution']
  vault: str
  usdc: float

class WsVaultWithdrawal(TypedDict):
  type: Literal['vaultWithdraw']
  vault: str
  user: str
  requestedUsd: float
  commission: float
  closingCost: float
  basis: float
  netWithdrawnUsd: float

class WsVaultLeaderCommission(TypedDict):
  type: Literal['vaultLeaderCommission']
  user: str
  usdc: float

class WsSpotTransfer(TypedDict):
  type: Literal['spotTransfer']
  token: str
  amount: float
  usdcValue: float
  user: str
  destination: str
  fee: float

class WsAccountClassTransfer(TypedDict):
  type: Literal['accountClassTransfer']
  usdc: float
  toPerp: bool

class WsSpotGenesis(TypedDict):
  type: Literal['spotGenesis']
  token: str
  amount: float

class WsRewardsClaim(TypedDict):
  type: Literal['rewardsClaim']
  amount: float

WsLedgerUpdate = (
  WsDeposit
  | WsWithdraw
  | WsInternalTransfer
  | WsSubAccountTransfer
  | WsLedgerLiquidation
  | WsVaultDelta
  | WsVaultWithdrawal
  | WsVaultLeaderCommission
  | WsSpotTransfer
  | WsAccountClassTransfer
  | WsSpotGenesis
  | WsRewardsClaim
)

class WsUserNonFundingLedgerUpdate(TypedDict):
  time: int
  hash: str
  delta: WsLedgerUpdate

class WsUserNonFundingLedgerUpdates(TypedDict, total=False):
  isSnapshot: bool
  user: str
  updates: list[WsUserNonFundingLedgerUpdate]
  ledgerUpdates: list[WsUserNonFundingLedgerUpdate]
  nonFundingLedgerUpdates: list[WsUserNonFundingLedgerUpdate]

class UserNonFundingLedgerUpdatesParams(TypedDict):
  user: str

adapter = pydantic.TypeAdapter(WsUserNonFundingLedgerUpdates)

class UserNonFundingLedgerUpdates(StreamsMixin):
  async def user_non_funding_ledger_updates(self, user: str):
    """Stream non-funding ledger updates.

    - `user`: Account address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    stream = await self.subscribe('userNonFundingLedgerUpdates', {'user': user})
    user_l = user.lower()
    def match(msg):
      if not isinstance(msg, dict):
        return True
      user_val = msg.get('user')
      return user_val is None or str(user_val).lower() == user_l
    stream = stream.filter(match)
    def mapper(msg) -> WsUserNonFundingLedgerUpdates:
      return adapter.validate_python(msg) if self.validate else msg
    return stream.map(mapper)
