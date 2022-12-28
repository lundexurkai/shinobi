
from __future__ import annotations

import math
from enum import IntEnum

from .stats import BoundedStat


def exp_for_level(level_base: int):
  exp_base= 100
  exp_mult = 1.1
  return math.floor(exp_base * (max(level_base - 10, 1) * exp_mult))

def get_total_exp(level_start: int, level_stop: int):  
  exp_total = 0
  for next_level in range(level_start + 1, level_stop):
    exp_total += exp_for_level(next_level)

  return exp_total

class Element(BoundedStat):

  _rank_descs = {
    0: "unplanted",
    20: "rooting",
    40: "established",
    60: "flowering",
    80: "blossoming",
    100: "full-grown",
  }
  
  type = "element"

  class Category(IntEnum):
    Basic = 1
    Advanced = 2

  @property
  def category(self) -> Element.Category:
    category = self.db["category"]
    if isinstance(category, str):
      return Element.Category[category.title()]
    return category
  
  @category.setter
  def category(self, value: Element.Category) -> None:
    self.db["category"] = value
  
  @property
  def exp(self) -> int:
    return self.db["exp"]
  
  @exp.setter
  def exp(self, value: int) -> None:
    self.db["exp"] = value
  
  @property
  def exp_cost(self):
    return exp_for_level(self.base)

  def get_total_exp(self, num_levels):
    return get_total_exp(self.base, self.base+num_levels)

  @property
  def exp_total(self) -> int:
    return self.db["exp_total"]
  
  @exp_total.setter
  def exp_total(self, value: int) -> None:
    self.db["exp_total"] = value

  @property
  def rank(self) -> str:
    high_desc = ""
    for bound, desc in self._rank_descs.items():
      high_desc = desc
      if self.actual <= bound:
        return desc
      
    return high_desc