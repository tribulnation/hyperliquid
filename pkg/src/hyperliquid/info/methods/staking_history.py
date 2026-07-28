"""Staking history: delegations, undelegations, deposits and withdrawals."""
from typing_extensions import Literal, Union
from decimal import Decimal
from hyperliquid.core import TypedDict
import pydantic
from hyperliquid.info.core import InfoMixin

class DelegationDelta(TypedDict):
  """Stake delegated to, or undelegated from, a validator."""
  validator: str
  """Validator address."""
  amount: Decimal
  """Amount delegated or undelegated (in HYPE)."""
  isUndelegate: bool
  """Whether stake was removed from the validator rather than added."""

class WithdrawalDelta(TypedDict):
  """A staking withdrawal, reported once per phase."""
  amount: Decimal
  """Amount withdrawn (in HYPE)."""
  phase: Literal['initiated', 'finalized']
  """Stage of the withdrawal. Finalization is a chain event with no user transaction,
  so `finalized` records carry an all-zero `hash`."""

class CDepositDelta(TypedDict):
  """A deposit into the staking balance."""
  amount: Decimal
  """Amount deposited (in HYPE)."""

class DelegateEntry(TypedDict):
  """A staking history entry describing a delegation change."""
  delegate: DelegationDelta

class WithdrawalEntry(TypedDict):
  """A staking history entry describing a withdrawal phase."""
  withdrawal: WithdrawalDelta

class CDepositEntry(TypedDict):
  """A staking history entry describing a staking deposit."""
  cDeposit: CDepositDelta

StakingHistoryDelta = Union[DelegateEntry, WithdrawalEntry, CDepositEntry]
"""What changed in a staking history entry.

Unlike most Hyperliquid payloads this is not tagged with a `type` field: the variant is
identified by which key is present. Check for the key rather than matching on a literal.
"""

class StakingHistoryEntry(TypedDict):
  """A single staking history record."""
  time: int
  """Time of the record, in milliseconds."""
  hash: str
  """Hash of the originating transaction. All-zero for `finalized` withdrawals, which
  are chain events with no user transaction, so it is not a unique key."""
  delta: StakingHistoryDelta
  """What changed."""

StakingHistoryResponse = list[StakingHistoryEntry]

adapter = pydantic.TypeAdapter(StakingHistoryResponse)

class StakingHistory(InfoMixin):
  async def staking_history(self, user: str) -> StakingHistoryResponse:
    """Return a user's staking history.

    Args:
      user: Account address.

    References:
      - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#query-a-users-staking-history)
    """
    r = await self.request({'type': 'delegatorHistory', 'user': user})
    return adapter.validate_python(r) if self.validate else r
