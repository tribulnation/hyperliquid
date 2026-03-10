# Error Handling

The client distinguishes between failure modes through explicit exception types.

## Common Error Categories

- `NetworkError`: connection failures, timeouts, and transport errors
- `AuthError`: authentication or signing failures
- `ApiError`: the remote API returned an application-level error
- `ValidationError`: the response shape did not match the expected schema
- `UserError`: incorrect local usage of the client
- `ValueError`: missing `HYPERLIQUID_PRIVATE_KEY` when using wallet-backed convenience constructors

## Recommended Pattern

```python
from hyperliquid.core import ApiError, AuthError, NetworkError, ValidationError

try:
  ...
except ValidationError:
  ...
except AuthError:
  ...
except ApiError:
  ...
except NetworkError:
  ...
```

## Operational Guidance

- retry transient network failures carefully
- do not blindly retry signing or authentication failures
- log validation failures because they often signal upstream API changes
- keep trading examples separate from harmless exchange actions like `noop()`
