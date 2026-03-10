from dataclasses import dataclass as _dataclass
from .order import PlaceOrder
from .cancel import CancelOrders
from .cancel_by_cloid import CancelByCloidOrders
from .schedule_cancel import ScheduleCancelOrders
from .modify_order import ModifyOrder
from .modify_orders import ModifyOrders
from .update_leverage import UpdateLeverage
from .update_isolated_margin import UpdateIsolatedMargin
from .usdc_transfer import UsdcTransfer
from .spot_transfer import SpotTransfer
from .withdraw3 import Withdraw3
from .usd_class_transfer import UsdClassTransfer
from .send_asset import SendAsset
from .send_to_evm_with_data import SendToEvmWithData
from .staking_deposit import StakingDeposit
from .staking_withdraw import StakingWithdraw
from .token_delegate import TokenDelegate
from .vault_transfer import VaultTransfer
from .approve_agent import ApproveAgent
from .approve_builder_fee import ApproveBuilderFee
from .twap_order import TwapOrder
from .twap_cancel import TwapCancel
from .reserve_request_weight import ReserveRequestWeight
from .noop import Noop
from .user_dex_abstraction import UserDexAbstraction
from .agent_enable_dex_abstraction import AgentEnableDexAbstraction
from .user_set_abstraction import UserSetAbstraction
from .agent_set_abstraction import AgentSetAbstraction
from .validator_l1_stream import ValidatorL1Stream

@_dataclass
class Exchange(
  PlaceOrder,
  CancelOrders,
  CancelByCloidOrders,
  ScheduleCancelOrders,
  ModifyOrder,
  ModifyOrders,
  UpdateLeverage,
  UpdateIsolatedMargin,
  UsdcTransfer,
  SpotTransfer,
  Withdraw3,
  UsdClassTransfer,
  SendAsset,
  SendToEvmWithData,
  StakingDeposit,
  StakingWithdraw,
  TokenDelegate,
  VaultTransfer,
  ApproveAgent,
  ApproveBuilderFee,
  TwapOrder,
  TwapCancel,
  ReserveRequestWeight,
  Noop,
  UserDexAbstraction,
  AgentEnableDexAbstraction,
  UserSetAbstraction,
  AgentSetAbstraction,
  ValidatorL1Stream,
):
  ...
