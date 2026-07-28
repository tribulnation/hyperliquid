"""Non-funding ledger updates: deposits, withdrawals, transfers, vault and staking flows."""
from typing_extensions import Annotated, AsyncIterable, Literal, TypeAlias, Union
from decimal import Decimal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin
from hyperliquid.info.pagination import paginate

PAGE_SIZE = 2000
"""Maximum number of entries `user_non_funding_ledger_updates` returns per call."""

class DepositDelta(TypedDict):
  """Funds deposited into the account."""
  type: Literal['deposit']
  usdc: Decimal
  """Amount deposited (in USDC)."""

class WithdrawDelta(TypedDict):
  """Funds withdrawn from the account."""
  type: Literal['withdraw']
  usdc: Decimal
  """Amount withdrawn (in USDC)."""
  nonce: int
  """Nonce of the withdrawal action."""
  fee: Decimal
  """Withdrawal fee (in USDC)."""

class InternalTransferDelta(TypedDict):
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

class SubAccountTransferDelta(TypedDict):
  """USDC transfer between an account and one of its sub-accounts."""
  type: Literal['subAccountTransfer']
  usdc: Decimal
  """Amount transferred (in USDC)."""
  user: str
  """Sender address."""
  destination: str
  """Recipient address."""

class AccountClassTransferDelta(TypedDict):
  """Transfer between the spot and perp wallets of the same account."""
  type: Literal['accountClassTransfer']
  usdc: Decimal
  """Amount transferred (in USDC)."""
  toPerp: bool
  """Whether the transfer moved funds into the perp wallet."""

class SpotTransferDelta(TypedDict):
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

class SendDelta(TypedDict):
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

class CStakingTransferDelta(TypedDict):
  """Transfer between the spot wallet and the staking balance."""
  type: Literal['cStakingTransfer']
  token: str
  """Staked token name."""
  amount: Decimal
  """Amount transferred (in token units)."""
  isDeposit: bool
  """Whether the transfer moved funds into staking."""

class LiquidatedPosition(TypedDict):
  """A single position closed by a liquidation."""
  coin: str
  """Asset name."""
  szi: Decimal
  """Signed size of the liquidated position (in base units)."""

class LiquidationDelta(TypedDict):
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

class VaultCreateDelta(TypedDict):
  """A vault was created by this account."""
  type: Literal['vaultCreate']
  vault: str
  """Vault address."""
  usdc: Decimal
  """Initial vault deposit (in USDC)."""
  fee: Decimal
  """Vault creation fee (in USDC)."""

class VaultDepositDelta(TypedDict):
  """Funds deposited into a vault."""
  type: Literal['vaultDeposit']
  vault: str
  """Vault address."""
  usdc: Decimal
  """Amount deposited (in USDC)."""

class VaultDistributionDelta(TypedDict):
  """Funds distributed from a vault to its depositors."""
  type: Literal['vaultDistribution']
  vault: str
  """Vault address."""
  usdc: Decimal
  """Amount distributed (in USDC)."""

class VaultWithdrawDelta(TypedDict):
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

class VaultLeaderCommissionDelta(TypedDict):
  """Commission earned as the leader of a vault."""
  type: Literal['vaultLeaderCommission']
  user: str
  """Vault leader address."""
  usdc: Decimal
  """Commission earned (in USDC)."""

class SpotGenesisDelta(TypedDict):
  """Tokens received from a spot deployment genesis distribution."""
  type: Literal['spotGenesis']
  token: str
  """Token name."""
  amount: Decimal
  """Amount received (in token units)."""

class RewardsClaimDelta(TypedDict):
  """Rewards claimed by the account."""
  type: Literal['rewardsClaim']
  amount: Decimal
  """Amount claimed (in token units)."""
  token: str
  """Token the rewards are denominated in. May be empty for legacy USDC claims."""

class BorrowLendDelta(TypedDict):
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

class ActivateDexAbstractionDelta(TypedDict):
  """Fee paid to activate balance abstraction on a perp dex."""
  type: Literal['activateDexAbstraction']
  dex: str
  """Perp dex name."""
  token: str
  """Token the fee is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

class AccountActivationGasDelta(TypedDict):
  """Gas charged to activate the account on HyperCore."""
  type: Literal['accountActivationGas']
  token: str
  """Token the gas is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

class DeployGasAuctionDelta(TypedDict):
  """Gas paid into a deploy auction."""
  type: Literal['deployGasAuction']
  token: str
  """Token the gas is denominated in."""
  amount: Decimal
  """Amount charged (in token units)."""

LedgerDelta: TypeAlias = Annotated[
  Union[
    DepositDelta,
    WithdrawDelta,
    InternalTransferDelta,
    SubAccountTransferDelta,
    AccountClassTransferDelta,
    SpotTransferDelta,
    SendDelta,
    CStakingTransferDelta,
    LiquidationDelta,
    VaultCreateDelta,
    VaultDepositDelta,
    VaultDistributionDelta,
    VaultWithdrawDelta,
    VaultLeaderCommissionDelta,
    SpotGenesisDelta,
    RewardsClaimDelta,
    BorrowLendDelta,
    ActivateDexAbstractionDelta,
    AccountActivationGasDelta,
    DeployGasAuctionDelta,
  ],
  pydantic.Discriminator('type'),
]
"""A single non-funding ledger delta, discriminated on `type`.

Hyperliquid adds ledger types over time, and an unrecognized `type` raises a
`ValidationError` rather than validating as an opaque value. This is deliberate: ledger
deltas move balances, so a silently-ignored new type would corrupt any accounting built on
this endpoint. Failing loudly surfaces the new type instead of hiding it.

Callers that must tolerate unmodeled types should validate each delta individually and
handle the failures explicitly, or use `validate=False` for raw payloads.
"""

class UserNonFundingLedgerEntry(TypedDict):
  """A single non-funding ledger update."""
  delta: LedgerDelta
  """What changed."""
  hash: str
  """Hash of the originating transaction. Not unique: one transaction can emit
  several deltas, so `(time, hash)` is not a primary key."""
  time: int
  """Time of the update, in milliseconds."""

UserNonFundingLedgerUpdatesResponse = list[UserNonFundingLedgerEntry]

adapter = pydantic.TypeAdapter(UserNonFundingLedgerUpdatesResponse)

class UserNonFundingLedgerUpdates(InfoMixin):
  async def user_non_funding_ledger_updates(
    self, user: str, start_time: int, *, end_time: int | None = None
  ) -> UserNonFundingLedgerUpdatesResponse:
    """Return a user's non-funding ledger updates.

    Args:
      user: Account address.
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
    """
    params: dict[str, object] = {
      'type': 'userNonFundingLedgerUpdates',
      'user': user,
      'startTime': start_time,
    }
    if end_time is not None:
      params['endTime'] = end_time
    r = await self.request(params)
    return adapter.validate_python(r) if self.validate else r

  async def user_non_funding_ledger_updates_paged(
    self, user: str, start_time: int, *, end_time: int | None = None
  ) -> AsyncIterable[UserNonFundingLedgerUpdatesResponse]:
    """Return a user's non-funding ledger updates, automatically paginating the results.

    A single call returns at most 2000 entries, keeping the oldest and silently dropping
    the rest, so any account with more history is truncated without an error. Prefer this
    over `user_non_funding_ledger_updates` whenever complete history matters.

    One transaction can emit several deltas on the same millisecond, so pages are
    advanced to the last timestamp seen rather than past it, and the re-fetched
    entries are dropped by position. `(time, hash)` is not used as a key because it
    is not unique, and hashing the body would collapse identical deltas.

    Args:
      user: Account address.
      start_time: Start time in milliseconds, inclusive.
      end_time: End time in milliseconds, inclusive.

    Raises:
      PaginationError: The range cannot be walked without losing entries.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-a-users-funding-history-or-non-funding-ledger-updates)
    """
    async def fetch(cursor: int) -> UserNonFundingLedgerUpdatesResponse:
      """Fetch one page of ledger updates starting at `cursor`."""
      return await self.user_non_funding_ledger_updates(user, cursor, end_time=end_time)
    async for page in paginate(
      fetch, start_time=start_time, end_time=end_time, page_size=PAGE_SIZE,
    ):
      yield page
