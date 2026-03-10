from dataclasses import dataclass as _dataclass
from .all_mids import AllMids
from .notification import Notification
from .web_data3 import WebData3
from .twap_states import TwapStates
from .clearinghouse_state import ClearinghouseState
from .open_orders import OpenOrders
from .candle import Candle
from .l2_book import L2Book
from .trades import Trades
from .order_updates import OrderUpdates
from .user_events import UserEvents
from .user_fills import UserFills
from .user_fundings import UserFundings
from .user_non_funding_ledger_updates import UserNonFundingLedgerUpdates
from .active_asset_ctx import ActiveAssetCtx
from .active_asset_data import ActiveAssetData
from .user_twap_slice_fills import UserTwapSliceFills
from .user_twap_history import UserTwapHistory
from .bbo import Bbo

@_dataclass
class Streams(
  AllMids,
  Notification,
  WebData3,
  TwapStates,
  ClearinghouseState,
  OpenOrders,
  Candle,
  L2Book,
  Trades,
  OrderUpdates,
  UserEvents,
  UserFills,
  UserFundings,
  UserNonFundingLedgerUpdates,
  ActiveAssetCtx,
  ActiveAssetData,
  UserTwapSliceFills,
  UserTwapHistory,
  Bbo,
):
  ...
