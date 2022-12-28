""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from shinobi.utils import fuzzy_search
from world.modifiers import find_modifier_class

if TYPE_CHECKING:
  from .modifiers import Modifier

class ModifierError(RuntimeError):
  pass

class ModifierHandler:
  ""

  def __init__(self, obj, attr_name: str, group: str, default=None, save_by_id=False) -> None:
    self.obj = obj
    self.attr_name = attr_name
    self.group = group
    self.default = default
    self.save_by_id = save_by_id
    self.modifier = None
    self.load()

  def load(self) -> None:
    flag = self.obj.attributes.get(self.attr_name, default=self.default)
    if flag is not None and (modifier_cls := find_modifier_class(flag, self.group)):
      self.modifier = modifier_cls(self)

  def save(self) -> None:
    if self.modifier:
      if self.save_by_id:
        flag = self.modifier.modifier_id
      else:
        flag = self.modifier.get_name()
      self.obj.attributes.add(self.attr_name, flag)
    else:
      self.obj.attributes.remove(self.attr_name)

  def get(self) -> Modifier | None:
    return self.modifier

  def set(self, flag: int | str, strict=False) -> Modifier | None:
    if (modifier_cls := find_modifier_class(flag, self.group)):
      self.modifier = modifier_cls(self)
      self.save()
      return self.modifier
    
    if strict:
      raise ModifierError(f"{self.group} {flag} not found.")

  def clear(self) -> None:
    self.modifier = None
    self.save()

  def all(self) -> list[Modifier]:
    if self.modifier:
      return [self.modifier]
    return []

class ModifierListHandler:
  ""

  @property
  def mod_ids(self):
    return {mod.modifier_id: mod for mod in self._modifiers}
  
  @property
  def mod_names(self):
    return {mod.get_name(): mod for mod in self._modifiers}
  
  def __init__(self, obj, attr_name: str, group: str, save_by_id=False) -> None:
    self.obj = obj
    self.attr_name = attr_name
    self.group = group
    self.save_by_id = save_by_id
    self._modifiers: list[Modifier] = []
    
    self.load()

  def load(self) -> None:
    flags = self.obj.attributes.get(self.attr_name, default=[])

    for flag in flags:
      if (modifier_cls := find_modifier_class(flag, self.group)):
        modifier = modifier_cls(self)
        self._modifiers.append(modifier)

  def save(self) -> None:
    if self.save_by_id:
      flags = sorted(self.mod_ids)
    else:
      flags = sorted(self.mod_names)
    
    if flags:
      self.obj.attributes.add(self.attr_name, flags)
    else:
      self.obj.attributes.remove(self.attr_name)

  def add(self, flag: int | str, strict=False):
    if (modifier_cls := find_modifier_class(flag, self.group)):
      modifier = modifier_cls(self)
      self._modifiers.append(modifier)
      self.save()
      return modifier
    
    if strict:
      raise ModifierError(f"{self.group} {flag} not found.")
  
  def get(self, flag: int | str, exact=True) -> Modifier | None:
    if isinstance(flag, int):
      if (mod := self.mod_ids.get(flag, None)):
        return mod
    else:
      if (mod := self.mod_names.get(flag, None)):
        return mod
      if (mod_name := fuzzy_search(flag, self.mod_names.keys(), exact)):
        return self.mod_names[mod_name]

  def has(self, flag: int | str):
    if (_ := self.get(flag)):
      return True
    else:
      return False

  def remove(self, flag: int | str, strict=False):
    if (modifier := self.get(flag, exact=True)):
      self._modifiers.remove(modifier)
      self.save()
      return modifier
    
    if strict:
      raise ModifierError(f"{self.group} {flag} not found.")

  def clear(self):
    if self.save_by_id:
      flags = list(self.mod_ids.keys())
    else:
      flags = list(self.mod_names.keys())
    
    for flag in flags:
      self.remove(flag)

  def all(self):
    return self._modifiers


class ModifierDictHandler(ModifierListHandler):
  "This class uses an inherited class `ModifierSaverDict` to implement a storage dict"

  def load(self) -> None:  
    self.flags_dict = self.obj.attributes.get(self.attr_name, default={})
    for flag in self.flags_dict.keys():
      if (modifier_cls := find_modifier_class(flag, self.group)):
        modifier = modifier_cls(self)
        self._modifiers.append(modifier)
  
  def save(self) -> None:
    pass
  
  def db(self, flag: int | str):
    if flag not in self.flags_dict:
      self.flags_dict[flag] = {}
    return self.flags_dict
  