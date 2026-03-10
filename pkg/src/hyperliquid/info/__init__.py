from dataclasses import dataclass as _dataclass
from .spot import SpotInfo
from .perps import PerpsInfo
from .methods import MethodsInfo

@_dataclass
class Info(SpotInfo, PerpsInfo, MethodsInfo):
  ...
