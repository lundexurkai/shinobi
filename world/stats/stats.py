""""""

from __future__ import annotations

from typing import Any

from evennia.utils.utils import lazy_property


class Stat:

  @property
  def obj(self):
    return self.handler.obj
  
  @lazy_property
  def db(self) -> dict[str, Any]:
    return self.handler.db(self.key)
  
  @property
  def name(self) -> str:
    return self.db["name"]
  
  @name.setter
  def name(self, value: str) -> None:
    self.db["name"] = value
  
  def __init__(self, handler, key: str):
    self.handler = handler
    self.key = key
  
  def bonus(self) -> int:
    out = 0
    for mod in self.obj.get_all_modifiers():
      out += mod.stat_bonus(self.obj, self.key)
    return out
  
  def mult(self) -> float: 
    out = 1.0
    for mod in self.obj.get_all_modifiers():
      out += mod.stat_multiplier(self.obj, self.key)
    return out
  
  def get_bonuses(self) -> tuple[int, float]:
    bonus, mult = 0, 1.0
    for mod in self.obj.get_all_modifiers():
      bonus += mod.stat_bonus(self.obj, self.key)
      mult += mod.stat_multiplier(self.obj, self.key)
    return bonus, mult

  @property
  def base(self) -> int:
    return self.db["base"]
  
  @base.setter
  def base(self, value: int) -> None:
    self.db["base"] = value
  
  def actual(self):
    bonus, mult = self.get_bonuses()
    return round((self.base + bonus) * mult)
  
  def set(self, value: int) -> int:
    self.base = value
    return self.base
  
  def modify(self, value: int) -> int:
    return self.set(self.base + value)

class BoundedStat(Stat):
  ""

  @property
  def max(self) -> int:
    return self.db["max"]
  
  @max.setter
  def max(self, value: int) -> None:
    self.db["max"] = value
  
  @property
  def min(self) -> int:
    return self.db["min"]
  
  @min.setter
  def min(self, value: int) -> None:
    self.db["min"] = value

  def __init__(self, handler, key: str):
    super().__init__(handler, key)
  
  def set(self, value: int) -> int:
    self.base = min(max(value, self.min), self.max)
    self.save()
    return self.base
  
  def modify(self, value: int) -> int:
    return self.set(self.base + value)

  def at_max(self): 
    return self.base == self.max
  
  def set_max(self):
    self.base = self.max

  def at_min(self): 
    return self.base == self.min
  
  def set_min(self):
    self.base = self.min
  

class DerivedStat(Stat):

  def __init__(self, handler, key: str):
    super().__init__(handler, key)

  @property
  def base(self) -> int:
    return super().base() + self.derived_base
  
  @property
  def derived_base(self) -> int:
    if (derived_func := getattr(self.handler, f"get_{self.key}", None)):
      return derived_func()
    return 0
  

class PoolStat(BoundedStat):

  @property
  def max(self) -> int:
    out = 0
    # self.db["max"] holds the max base value.
    if "max" in self.db:
      out += self.db["max"]
    # then we check for a dervied max base value to add.
    if max_func := getattr(self.handler, f"get_{self.name.lower()}", None):
      out += max_func()
    return out
  
  @property
  def min(self) -> int:
    out = 0
    if "min" in self.db:
      out = self.db["min"]
    if min_func := getattr(self.handler, f"get_{self.name.lower()}_min", None):
      out += min_func()
    return out