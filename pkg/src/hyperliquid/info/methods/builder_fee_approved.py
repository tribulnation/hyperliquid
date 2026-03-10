import pydantic
from hyperliquid.info.core import InfoMixin

BuilderFeeApprovedResponse = int

adapter = pydantic.TypeAdapter(BuilderFeeApprovedResponse)

class BuilderFeeApproved(InfoMixin):
  async def builder_fee_approved(
    self, user: str, builder: str
  ) -> BuilderFeeApprovedResponse:
    """Return the max builder fee approved.

    - `user`: Account address.
    - `builder`: Builder address.

    > [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#check-builder-fee-approval)
    """
    r = await self.request({
      'type': 'maxBuilderFee',
      'user': user,
      'builder': builder,
    })
    return adapter.validate_python(r) if self.validate else r
