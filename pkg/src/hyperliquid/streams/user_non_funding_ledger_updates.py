"""Stream of non-funding ledger updates: deposits, withdrawals, transfers, vault and staking flows."""
from typing_extensions import Annotated, Literal, TypeAlias, Union
from decimal import Decimal
from hyperliquid.core import TypedDict
import pydantic

from hyperliquid.streams.core import StreamsMixin
from typed_core.util import StreamManager

class LiquidatedPosition(TypedDict):
  """A single position closed by a liquidation."""
  coin: str
  """Asset name."""
  szi: Decimal
  """Signed size of the liquidated position (in base units)."""

class WsDeposit(TypedDict):
  """Funds deposited into the account."""
  type: Literal['deposit']
  usdc: Decimal
  """Amount deposited (in USDC)."""

class WsWithdraw(TypedDict):
  """Funds withdrawn from the account."""
  type: Literal['withdraw']
  usdc: Decimal
  """Amount withdrawn (in USDC)."""
  nonce: int
  """Nonce of the withdrawal action."""
  fee: Decimal
  """Withdrawal fee (in USDC)."""

class WsInternalTransfer(TypedDict):
  """USDC transfer between two Hyperliquid accounts."""
  type: Literal['internalTransfer']
  usdc: Decimal
  """Amount transferred (in USDC)."""
  user: str
  """Sender address."""
  destination: str
  """Recipient address."""
  fee: Decimal
  """Transfer fee (in USDC)."""

class WsSubAccountTransfer(TypedDict):
  """USDC transfer between an account and one of its sub-accounts."""
  type: Literal['subAccountTransfer']
  usdc: Decimal
  """Amount transferred (in USDC)."""
  user: str
  """Sender address."""
  destination: str
  """Recipient address."""

class WsAccountClassTransfer(TypedDict):
  """Transfer between the spot and perp wallets of the same account."""
  type: Literal['accountClassTransfer']
  usdc: Decimal
  """Amount transferred (in USDC)."""
  toPerp: bool
  """Whether the transfer moved funds into the perp wallet."""

class WsSpotTransfer(TypedDict):
  """Spot token transfer between two accounts."""
  type: Literal['spotTransfer']
  token: str
  """Token name."""
  amount: Decimal
  """Amount transferred (in token units)."""
  usdcValue: Decimal
  """Value of the transfer (in USDC)."""
  user: str
  """Sender address."""
  destination: str
  """Recipient address."""
  fee: Decimal
  """Transfer fee, denominated in `feeToken`."""
  nativeTokenFee: Decimal
  """Portion of the fee paid in the native token."""
  feeToken: str
  """Token the fee is denominated in. May be empty when no fee was charged."""
  nonce: int | None
  """Nonce of the transfer action, if any."""

class WsSend(TypedDict):
  """Token transfer between accounts, possibly across perp dexs."""
  type: Literal['send']
  token: str
  """Token name."""
  amount: Decimal
  """Amount sent (in token units)."""
  usdcValue: Decimal
  """Value of the transfer (in USDC)."""
  user: str
  """Sender address."""
  destination: str
  """Recipient address."""
  sourceDex: str
  """Perp dex the funds were sent from. Empty for the main perp wallet, `'spot'` for the spot wallet."""
  destinationDex: str
  """Perp dex the funds were sent to. Empty for the main perp wallet, `'spot'` for the spot wallet."""
  fee: Decimal
  """Transfer fee, denominated in `feeToken`."""
  nativeTokenFee: Decimal
  """Portion of the fee paid in the native token."""
  feeToken: str
  """Token the fee is denominated in. May be empty when no fee was charged."""
  nonce: int
  """Nonce of the send action."""

class WsCStakingTransfer(TypedDict):
  """Transfer between the spot wallet and the staking balance."""
  type: Literal['cStakingTransfer']
  token: str
  """Staked token name."""
  amount: Decimal
  """Amount transferred (in token units)."""
  isDeposit: bool
  """Whether the transfer moved funds into staking."""

class WsLedgerLiquidation(TypedDict):
  """The account was liquidated."""
  type: Literal['liquidation']
  accountValue: Decimal
  """Account value at liquidation time (in USDC)."""
  liquidatedNtlPos: Decimal
  """Total notional of the liquidated positions (in USDC)."""
  leverageType: Literal['Cross', 'Isolated']
  """Margin mode of the liquidated positions."""
  liquidatedPositions: list[LiquidatedPosition]
  """Positions closed by the liquidation."""

class WsVaultCreate(TypedDict):
  """A vault was created by this account."""
  type: Literal['vaultCreate']
  vault: str
  """Vault address."""
  usdc: Decimal
  """Initial vault deposit (in USDC)."""
  fee: Decimal
  """Vault creation fee (in USDC)."""

class WsVaultDelta(TypedDict):
  """Funds deposited into, or distributed from, a vault."""
  type: Literal['vaultDeposit', 'vaultDistribution']
  vault: str
  """Vault address."""
  usdc: Decimal
  """Amount moved (in USDC)."""

class WsVaultWithdrawal(TypedDict):
  """Funds withdrawn from a vault."""
  type: Literal['vaultWithdraw']
  vault: str
  """Vault address."""
  user: str
  """Address withdrawing from the vault."""
  requestedUsd: Decimal
  """Amount requested (in USDC)."""
  commission: Decimal
  """Leader commission charged on the withdrawal (in USDC)."""
  closingCost: Decimal
  """Cost of closing the vault's positions (in USDC)."""
  basis: Decimal
  """Cost basis of the withdrawn share (in USDC)."""
  netWithdrawnUsd: Decimal
  """Amount actually withdrawn after costs (in USDC)."""

class WsVaultLeaderCommission(TypedDict):
  """Commission earned as the leader of a vault."""
  type: Literal['vaultLeaderCommission']
  user: str
  """Vault leader address."""
  usdc: Decimal
  """Commission earned (in USDC)."""

class WsSpotGenesis(TypedDict):
  """Tokens received from a spot deployment genesis distribution."""
  type: Literal['spotGenesis']
  token: str
  """Token name."""
  amount: Decimal
  """Amount received (in token units)."""

class WsRewardsClaim(TypedDict):
  """Rewards claimed by the account."""
  type: Literal['rewardsClaim']
  amount: Decimal
  """Amount claimed (in token units)."""
  token: str
  """Token the rewards are denominated in. May be empty for legacy USDC claims."""

class WsBorrowLend(TypedDict):
  """Supply or withdrawal on the borrow/lend market."""
  type: Literal['borrowLend']
  token: str
  """Token name."""
  operation: str
  """Operation performed, e.g. `'supply'` or `'withdraw'`."""
  amount: Decimal
  """Principal amount (in token units)."""
  interestAmount: Decimal
  """Interest accrued (in token units)."""

class WsActivateDexAbstraction(TypedDict):
  """Fee paid to activate balance abstraction on a perp dex."""
  type: Literal['activateDexAbstraction']
  dex: str
  """Perp dex name."""
  token: str
  """Token the fee is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

class WsAccountActivationGas(TypedDict):
  """Gas charged to activate the account on HyperCore."""
  type: Literal['accountActivationGas']
  token: str
  """Token the gas is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

class WsDeployGasAuction(TypedDict):
  """Gas paid into a deploy auction."""
  type: Literal['deployGasAuction']
  token: str
  """Token the gas is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

WsLedgerUpdate: TypeAlias = Annotated[
  Union[
    WsDeposit,
    WsWithdraw,
    WsInternalTransfer,
    WsSubAccountTransfer,
    WsAccountClassTransfer,
    WsSpotTransfer,
    WsSend,
    WsCStakingTransfer,
    WsLedgerLiquidation,
    WsVaultCreate,
    WsVaultDelta,
    WsVaultWithdrawal,
    WsVaultLeaderCommission,
    WsSpotGenesis,
    WsRewardsClaim,
    WsBorrowLend,
    WsActivateDexAbstraction,
    WsAccountActivationGas,
    WsDeployGasAuction,
  ],
  pydantic.Discriminator('type'),
]
"""A single non-funding ledger delta, discriminated on `type`.

Hyperliquid adds ledger types over time, and an unrecognized `type` raises a
`ValidationError` rather than validating as an opaque value. This is deliberate: ledger
deltas move balances, so a silently-ignored new type would corrupt any accounting built on
this stream. Failing loudly surfaces the new type instead of hiding it.

Callers that must tolerate unmodeled types should use `validate=False` for raw payloads.
"""

class WsUserNonFundingLedgerUpdate(TypedDict):
  """A single non-funding ledger update."""
  time: int
  """Time of the update, in milliseconds."""
  hash: str
  """Hash of the originating transaction. Not unique: one transaction can emit
  several deltas, so `(time, hash)` is not a primary key."""
  delta: WsLedgerUpdate
  """What changed."""

class WsUserNonFundingLedgerUpdates(TypedDict, total=False):
  """Non-funding ledger updates message."""
  isSnapshot: bool
  """Whether this message is the initial snapshot of past updates."""
  user: str
  """Account address."""
  updates: list[WsUserNonFundingLedgerUpdate]
  ledgerUpdates: list[WsUserNonFundingLedgerUpdate]
  nonFundingLedgerUpdates: list[WsUserNonFundingLedgerUpdate]

class UserNonFundingLedgerUpdatesParams(TypedDict):
  """Subscription parameters."""
  user: str

adapter = pydantic.TypeAdapter(WsUserNonFundingLedgerUpdates)

class UserNonFundingLedgerUpdates(StreamsMixin):
  def user_non_funding_ledger_updates(self, user: str):
    """Stream non-funding ledger updates.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/websocket#subscriptions)
    """
    return StreamManager(lambda: self._user_non_funding_ledger_updates_impl(user))

  async def _user_non_funding_ledger_updates_impl(self, user: str):
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
