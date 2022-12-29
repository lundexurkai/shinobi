""""""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

from shinobi.techniques import find_technique

if TYPE_CHECKING:
  from shinobi.styles.styles import Style

  from .techniques import Technique

class TechniqueError(RuntimeError):
  """
  """
  pass

class TechniqueHandler:
  """
  """

  def __init__(self, obj, attr_name="techniques", attr_category="techniques") -> None:
    self.techniques_data = obj.attributes.get(attr_name, category=attr_category)
    if not self.techniques_data:
      obj.attributes.add(attr_name, {}, category=attr_category)
      self.techniques_data = obj.attributes.get(attr_name, category=attr_category)
    
    self.obj = obj
    self._cache: dict[str, Technique] = {}

  def add(self, technique_name:str, force=True, quiet=False) -> None:
    if not (technique := find_technique(technique_name)):
      raise TechniqueError(f"Technique not found: {technique_name}")
    else:
      technique_name = technique.get_name()

    if technique_name in self.techniques_data:
      if force:
        self.remove(technique_name)
      else:
        raise TechniqueError(f"Techhnique '{technique_name}' already exists.")

    technique_data = {"exp": 0, "level": technique.min_level}
    self.techniques_data[technique_name] = technique_data
  
    if not quiet:
      self.obj.msg(f"|CThe technique |n'|w{technique.name}|n'|C has been added|n.")

  def get(self, technique_name:str) -> Technique | None:
    technique = self._cache.get(technique_name)
    if not technique and technique_name in self.techniques_data:
      if not (technique_cls := find_technique(technique_name)):
        raise TechniqueError(f"Technique not found: {technique_name}")
      technique = self._cache[technique_name] = technique_cls(self)
    return technique
  
  def has(self, technique_name: str) -> bool:
    if not (technique := find_technique(technique_name)):
      return False
    else:
      technique_name = technique.get_name()
    return technique_name in self.techniques_data.keys()

  def db(self, technique_name:str) -> dict[str, Any]:
    if technique_name not in self.techniques_data:
      self.techniques_data[technique_name] = {}
    return self.techniques_data[technique_name]

  def get_all(self, style: Type[Style]=None) -> dict[str, Technique]:
    for technique_name in self.all():
      if technique_name not in self._cache.keys():
        self.get(technique_name)
    
    techniques = self._cache
    if style is not None:
      return dict(filter(lambda i: i[1].style == style.get_name(), techniques.items()))
    else:
      return techniques

  def remove(self, technique_name:str, quiet=False) -> None:
    if not (technique := find_technique(technique_name)):
      raise TechniqueError(f"Technique not found: {technique_name}")
    else:
      technique_name = technique.get_name()

    if technique_name not in self.techniques_data:
      return
    
    if technique_name in self._cache:
      del self._cache[technique_name]

    del self.techniques_data[technique_name]

    if not quiet:
      self.obj.msg(f"|RThe technique |n'|w{technique.name}|n'|R has been removed|n.")

  def clear(self) -> None:
    for technique_name in self.all():
      self.remove(technique_name)

  def all(self) -> list[str]:
    return list(self.techniques_data.keys())