"""Time-cursor pagination shared by the `*_paged` info helpers.

Hyperliquid's time-ranged info endpoints return the *oldest* entries of
`[start_time, end_time]`, capped at a per-endpoint page size, so walking a long
range means re-issuing the request with the cursor moved forward.

Timestamps are milliseconds and are not unique: a single millisecond routinely
holds dozens of entries. Moving the cursor to `last_time + 1` therefore drops
every entry that shares the last millisecond of a truncated page, silently and
permanently. The cursor is instead moved to `last_time`, which re-fetches that
millisecond in full, and the already-yielded prefix is removed.

The overlap is removed *by position*, not by an id or a content hash, because
neither is trustworthy:

- `tid` is not unique for fills. Every `Spot Dust Conversion` fill carries the
  sentinel `tid: 0`, so keying on it collapses unrelated fills.
- Funding entries carry no id at all, and for ledger updates `(time, hash)` is
  explicitly not a primary key: one transaction can emit several deltas.
- Content hashing would additionally collapse records that are legitimately
  identical, which nothing in the payloads rules out.

Position is safe because the endpoints return entries in ascending time order,
`start_time` is inclusive, and the relative order of entries sharing a
millisecond is stable across requests. The entries already yielded for the
cursor millisecond are therefore exactly the prefix of the next response, and
that prefix is verified on every page rather than assumed.

Callers must pass the endpoint's real page cap as `page_size`. It is the signal
that separates "this page is short because the range is exhausted" from "this
page is short because it was cut", and declaring it larger than the true cap
would reintroduce silent loss.
"""
from typing_extensions import Any, AsyncIterable, Awaitable, Callable, Mapping, TypeVar
from hyperliquid.core import PaginationError

Entry = TypeVar('Entry', bound=Mapping[str, Any])

async def paginate(
  fetch: Callable[[int], Awaitable[list[Entry]]], *,
  start_time: int, end_time: int | None, page_size: int,
) -> AsyncIterable[list[Entry]]:
  """Walk a time-ranged Hyperliquid endpoint, yielding every entry exactly once.

  Args:
    fetch: Fetch one page starting at the given timestamp, inclusive. It must
      apply the same `end_time` on every call.
    start_time: Start time in milliseconds, inclusive.
    end_time: End time in milliseconds, inclusive.
    page_size: Maximum number of entries the endpoint returns per call.

  Raises:
    PaginationError: The upstream order of entries sharing a millisecond changed
      mid-sweep, or a single millisecond fills a whole page, so the rest of that
      millisecond is unreachable and continuing would drop it.

  References:
    - [Hyperliquid API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
  """
  cursor = start_time
  overlap: list[Entry] = []
  while end_time is None or cursor <= end_time:
    page = await fetch(cursor)
    if not page:
      return
    if page[:len(overlap)] != overlap:
      raise PaginationError(
        f'Hyperliquid returned different entries for timestamp {cursor} than it '
        'did on the previous page. Pagination relies on the order of entries '
        'sharing a timestamp being stable across requests; it was not, so the '
        'sweep stopped instead of dropping or duplicating entries.'
      )
    fresh = page[len(overlap):]
    if fresh:
      yield fresh
    last_time = max(entry['time'] for entry in page)
    if last_time > cursor:
      cursor = last_time
      overlap = [entry for entry in page if entry['time'] == last_time]
    elif len(page) >= page_size:
      # Every entry of a full page shares `cursor`, so the page was truncated
      # inside that millisecond. The endpoint pages by time only, so the rest of
      # it is unreachable and moving on would drop it.
      raise PaginationError(
        f'Timestamp {cursor} holds at least {len(page)} entries, filling a whole '
        'page. Hyperliquid pages by time only, so the rest of that millisecond '
        'cannot be requested, and the sweep stopped instead of skipping it. '
        f'Resume from {cursor + 1} to continue while accepting that loss.'
      )
    else:
      # A page shorter than `page_size` was not truncated, so every entry at
      # `cursor` is already yielded and the millisecond can be stepped over.
      cursor += 1
      overlap = []
