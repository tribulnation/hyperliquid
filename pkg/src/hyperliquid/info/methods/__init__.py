from dataclasses import dataclass as _dataclass
from .all_mids import AllMids
from .open_orders import OpenOrders
from .frontend_open_orders import FrontendOpenOrders
from .user_fills import UserFills
from .user_fills_by_time import UserFillsByTime
from .user_rate_limit import UserRateLimit
from .order_status import OrderStatusInfo
from .builder_fee_approved import BuilderFeeApproved
from .user_historical_orders import UserHistoricalOrders
from .user_twap_slice_fills import UserTwapSliceFills
from .sub_accounts import SubAccounts
from .vault_details import VaultDetails
from .user_vault_equities import UserVaultEquities
from .user_role import UserRole
from .user_portfolio import UserPortfolio
from .user_referral import UserReferral
from .staking_delegations import StakingDelegations
from .staking_summary import StakingSummary
from .staking_history import StakingHistory
from .staking_rewards import StakingRewards
from .user_dex_abstraction import UserDexAbstraction
from .user_abstraction import UserAbstraction
from .aligned_quote_token_info import AlignedQuoteTokenInfo
from .borrow_lend_user_state import BorrowLendUserState
from .user_fees import UserFees
from .l2_book import L2Book
from .candle_snapshot import CandleSnapshot
from .borrow_lend_reserve_state import BorrowLendReserveState
from .all_borrow_lend_reserve_states import AllBorrowLendReserveStates

@_dataclass
class MethodsInfo(
  AllMids,
  OpenOrders,
  FrontendOpenOrders,
  UserFills,
  UserFillsByTime,
  UserRateLimit,
  OrderStatusInfo,
  BuilderFeeApproved,
  UserHistoricalOrders,
  UserTwapSliceFills,
  SubAccounts,
  VaultDetails,
  UserVaultEquities,
  UserRole,
  UserPortfolio,
  UserReferral,
  StakingDelegations,
  StakingSummary,
  StakingHistory,
  StakingRewards,
  UserDexAbstraction,
  UserAbstraction,
  AlignedQuoteTokenInfo,
  BorrowLendUserState,
  UserFees,
  L2Book,
  CandleSnapshot,
  BorrowLendReserveState,
  AllBorrowLendReserveStates,
):
  ...
