from dataclasses import dataclass as _dataclass
from .perp_dexs import PerpDexs
from .perp_meta import PerpMeta
from .perp_meta_and_asset_ctxs import PerpMetaAndAssetCtxs
from .clearinghouse_state import ClearinghouseState
from .user_funding import UserFunding
from .user_non_funding_ledger_updates import UserNonFundingLedgerUpdates
from .funding_history import FundingHistory
from .predicted_fundings import PredictedFundings
from .perps_at_open_interest_cap import PerpsAtOpenInterestCap
from .perp_deploy_auction_status import PerpDeployAuctionStatus
from .active_asset_data import ActiveAssetData
from .perp_dex_limits import PerpDexLimits
from .perp_dex_status import PerpDexStatus
from .all_perp_metas import AllPerpMetas
from .perp_annotation import PerpAnnotation
from .perp_categories import PerpCategories

@_dataclass
class PerpsInfo(
  PerpDexs,
  PerpMeta,
  PerpMetaAndAssetCtxs,
  ClearinghouseState,
  UserFunding,
  UserNonFundingLedgerUpdates,
  FundingHistory,
  PredictedFundings,
  PerpsAtOpenInterestCap,
  PerpDeployAuctionStatus,
  ActiveAssetData,
  PerpDexLimits,
  PerpDexStatus,
  AllPerpMetas,
  PerpAnnotation,
  PerpCategories,
):
  ...
