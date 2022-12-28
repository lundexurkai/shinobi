""""""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

from shinobi.stats import STAT_TYPES, STATS

if TYPE_CHECKING:
  from .stats import Stat

class StatError(RuntimeError):
  pass

class StatHandler:

  def __init__(self, obj, attr_name="stats", attr_category="stats") -> None:

    self.stats_data = obj.attributes.get(attr_name, category=attr_category)
    if not self.stats_data:
      obj.attributes.add(attr_name, {}, category=attr_category)
      self.stats_data = obj.attributes.get(attr_name, category=attr_category)
    
    self.obj = obj
    self._cache: dict[str, Stat] = {}

  def init_defaults(self):
    for stat_key, stat_properties in STATS.items():
      self.add(stat_key, **stat_properties)

  def _get_stat_class(self, type: str):
    if not (stat_cls := STAT_TYPES.get(type, None)):
      raise StatError(f"Stat type '{type}' not found.")
    else:
      return stat_cls

  def add(self, stat_key: str, name=None, type="static", force=True, **stat_properties):
    if stat_key in self.stats_data:
      if force:
        self.remove(stat_key)
      else:
        raise StatError(f"Stat '{stat_key}' already exists.")

    if type not in STAT_TYPES:
      raise StatError(f"Stat type '{type}' not found.")
    
    stat_properties["name"] = stat_key.title() if not name else name
    stat_properties["type"] = type

    self.stats_data[stat_key] = stat_properties
  
  def remove(self, stat_key:str):
    if stat_key not in self.stats_data:
      return
    
    if stat_key in self._cache:
      del self._cache[stat_key]
    del self.stats_data[stat_key]

  def get(self, stat_key:str):
    stat = self._cache.get(stat_key)
    if not stat and stat_key in self.stats_data:
      stat_cls = self._get_stat_class(self.stats_data[stat_key]["type"])
      stat = self._cache[stat_key] = stat_cls(self, stat_key)
    return stat
  
  def get_all(self, type=None) -> dict[str, Stat]:
    stats_data = dict(self.stats_data)
    for stat_key in stats_data:
      if stat_key not in self._cache.keys():
        self.get(stat_key)
    
    stats = self._cache
    if type is not None:
      return dict(filter(lambda i: i[1].type == type, stats.items()))
    else:
      return stats

  def db(self, stat_key: str):
    if stat_key not in self.stats_data:
      self.stats_data[stat_key] = {}
    return self.stats_data[stat_key]
  
  def clear(self):
    for stat_key in self.all():
      self.remove(stat_key)
    
  def all(self):
    return list(self.stats_data.keys())

  # derived calculations
  def get_accuracy(self):
    return 0
  
  def get_readiness(self):
    return 0

  # pools calculations
  def get_health_min(self):
    min_hp = 0
    if (hp := self.get("hp")):
      min_hp = round(hp.max * -0.1)
    return min_hp
  
  def get_health(self):
    return 0
  
  def get_chakra(self):
    return 0
  
  def get_energy(self):
    return 0
  
  def get_capacity(self):
    return 0
  
  def get_reserve(self):
    return 0
  
