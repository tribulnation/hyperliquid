from typed_core import Error, ApiError, AuthError, NetworkError, RateLimited, ValidationError, LogicError

class PaginationError(Error):
  """A paginated sweep could not continue without silently losing entries.

  Raised by the `*_paged` info helpers when the upstream endpoint cannot be
  walked safely: either the order of entries sharing a millisecond changed
  between requests, or a single millisecond holds a whole page of entries, in
  which case the endpoint has no way to express the rest of that millisecond.

  Stopping is deliberate. The alternative is to skip past the millisecond, which
  drops entries with no error and no gap indicator.
  """
  def __str__(self):
    return super().__str__()
