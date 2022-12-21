"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from evennia.utils.utils import callables_from_module, inherits_from

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

_TRAIT_CLASSES: dict[str, Type[Trait]] = {}

def _load_traits():
  "Delayed loading of trait classes."
  
  from django.conf import settings

  global _TRAIT_CLASSES
  if not _TRAIT_CLASSES:
    for path in settings.TRAIT_MODULES:
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Trait):
          _TRAIT_CLASSES[cls.name] = cls

class TraitError(RuntimeError):
  "Trait error"
  pass

class Trait:
  name = "unknown"
  desc = "No description available."

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()


class TraitHandler:
  """
  This class handles keep track of all the known traits.
  """

  tag_category = "traits"

  def __init__(self, char: Character) -> None:
    _load_traits()

    self.char = char
  
  def add(self, name:str):
    "Adds a trait to handler by name."
    if not self.has(name):
      self.char.tags.add(name, category=self.tag_category)

  def remove(self, name:str):
    "Removes a trait from the handler by name."
    if self.has(name):
      self.char.tags.remove(name, category="trait")
  
  def get(self, name: str):
    "Returns the trait class if trait is found."
    return _TRAIT_CLASSES.get(name)

  def has(self, name: str) -> bool:
    "Returns True if the name is found in traits otherwise False."
    return self.char.tags.has(name, category=self.tag_category)

  def all(self):
    "Returns a list of trait names, if any."
    return self.char.tags.get(category=self.tag_category, return_list=True)

  def clear(self):
    "Clears all traits from the handler."
    self.char.tags.clear(category=self.tag_category)
