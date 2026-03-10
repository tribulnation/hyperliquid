from dataclasses import dataclass as _dataclass
from .spot_meta import SpotMeta
from .spot_meta_and_asset_ctxs import SpotMetaAndAssetCtxs
from .spot_clearinghouse_state import SpotClearinghouseState
from .spot_deploy_state import SpotDeployState
from .spot_pair_deploy_auction_status import SpotPairDeployAuctionStatus
from .token_details import TokenDetails

@_dataclass
class SpotInfo(
  SpotMeta,
  SpotMetaAndAssetCtxs,
  SpotClearinghouseState,
  SpotDeployState,
  SpotPairDeployAuctionStatus,
  TokenDetails,
):
  ...
