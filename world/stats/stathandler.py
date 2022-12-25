""""""

from __future__ import annotations

from typing import Any, Type

from .stats import BoundedStat, DerivedStat, PoolStat, Stat

_STAT_CLASSES: dict[str, Type[Stat]] = {
  "static": Stat,
  "bound": BoundedStat,
  "derived": DerivedStat,
  "pool": PoolStat,
  
}

_STATS: dict[str, dict[str, Any]] = {

  "str": {"type": "static", "base": 1, "name": "Strength"},
  "dex": {"type": "static", "base": 1, "name": "Dexterity"},
  "end": {"type": "static", "base": 1, "name": "Endurance"},
  "int": {"type": "static", "base": 1, "name": "Intelligence"},
  "per": {"type": "static", "base": 1, "name": "Perception"},
  "wit": {"type": "static", "base": 1, "name": "Wits"},
  "spi": {"type": "static", "base": 1, "name": "Spirit"},
  "pre": {"type": "static", "base": 1, "name": "Precision"},
  "man": {"type": "static", "base": 1, "name": "Manipulation"},
  "ref": {"type": "static", "base": 1, "name": "Reflexes"},

  "acc": {"type": "derived", "base": 0, "name": "Accuracy"},
  "rea": {"type": "derived", "base": 0, "name": "Readiness"},
  
  "hun": {"type": "bound", "min": 0, "max": 100, "base": 100, "name": "Hunger"},
  "thi": {"type": "bound", "min": 0, "max": 100, "base": 100, "name": "Thrist"},
  "fat": {"type": "bound", "min": 0, "max": 100, "base": 0, "name": "Fatigue"},
  
  "hp": {"type": "pool", "max": 50, "base": 50, "name": "Health"},
  "ch": {"type": "pool", "max": 10, "base": 10, "name": "Chakra"},
  "en": {"type": "pool", "max": 100, "base": 100, "name": "Energy"},
  "cp": {"type": "pool", "max": 100, "base": 100, "name": "Capacity"},
  "re": {"type": "pool", "max": 0, "base": 0, "name": "Reserve"},
  
}

class StatError(RuntimeError):
  pass

class StatHandler:

  def __init__(self, obj, attr_name="stats") -> None:
    if not obj.attributes.has(attr_name):
      obj.attributes.add(attr_name, {})
    
    self.stats_data = obj.attributes.get(attr_name)
    self.obj = obj
    self._cache: dict[str, Stat] = {}

  def init_stats(self):
    for stat_key, stat_properties in _STATS.items():
      self.add(stat_key, **stat_properties)

  def _get_stat_class(self, type: str):
    if (stat_cls := _STAT_CLASSES.get(type, None)):
      return stat_cls
    raise StatError(f"Stat type '{type}' not found.")

  def add(self, stat_key: str, name=None, type="static", force=True, **stat_properties):
    if stat_key in self.stats_data:
      if force:
        self.remove(stat_key)
      else:
        raise StatError(f"Stat '{stat_key}' already exists.")

    if type not in _STAT_CLASSES:
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
      hp: PoolStat
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
  
