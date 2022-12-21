"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from evennia.utils.utils import callables_from_module, inherits_from

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

_BACKGROUND_CLASSES: dict[str, Type[Background]] = {}

def _load_backgrounds():
  "Delayed loading of background classes."
  
  from django.conf import settings

  global _BACKGROUND_CLASSES
  if not _BACKGROUND_CLASSES:
    for path in settings.BACKGROUND_MODULES:
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Background):
          _BACKGROUND_CLASSES[cls.name] = cls

class BackgroundError(RuntimeError):
  "Background error"
  pass

class Background:
  name = "unknown background"
  desc = "No description available."

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()


class BackgroundHandler:
  """
  This class handles keep track of all the known backgrounds.
  """

  tag_category = "backgrounds"

  def __init__(self, char: Character) -> None:
    _load_backgrounds()
    self.char = char
  
  def add(self, name:str):
    "Adds a background to handler by name."
    if not self.has(name):
      self.char.tags.add(name, category=self.tag_category)

  def remove(self, name:str):
    "Removes a background from the handler by name."
    if self.has(name):
      self.char.tags.remove(name, category="background")
  
  def get(self, name: str):
    "Returns the background class if background is found."
    return _BACKGROUND_CLASSES.get(name)

  def has(self, name: str) -> bool:
    "Returns True if the name is found in backgrounds otherwise False."
    return self.char.tags.has(name, category=self.tag_category)

  def all(self):
    "Returns a list of background names, if any."
    return self.char.tags.get(category=self.tag_category, return_list=True)

  def clear(self):
    "Clears all backgrounds from the handler."
    self.char.tags.clear(category=self.tag_category)