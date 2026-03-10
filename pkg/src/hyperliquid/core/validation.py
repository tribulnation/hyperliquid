from typing_extensions import TypedDict as _TypedDict
import pydantic

@pydantic.with_config({'extra': 'allow'})
class TypedDict(_TypedDict):
  ...