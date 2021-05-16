from typing import List

class PriceInfo:
  value: float
  average_gain_percentage: float

class Market:
  values: List[List[PriceInfo]] = []