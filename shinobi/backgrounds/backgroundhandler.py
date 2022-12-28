"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from shinobi.backgrounds import find_background

if TYPE_CHECKING:
  from shinobi.backgrounds.backgrounds import Background
  from typeclasses.characters.characters import Character

class BackgroundError(RuntimeError):
  "Background error"
  pass


class BackgroundHandler:
  """
  This class handles keep track of all the known backgrounds.
  """

  tag_category = "backgrounds"

  def __init__(self, char: Character) -> None:
    self.char = char
  
  def add(self, background_name:str, quiet=False) -> None:
    "Adds a background to handler by name."

    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      background_name = background.get_name()

    if self.has(background_name):
      return
    
    self.char.tags.add(background_name, category=self.tag_category)

    if not quiet:
      self.char.msg(f"Background has been gained: {background.name}")

    if background.traits:
      for trait_name in background.traits:
        self.char.traits.add(trait_name)

  def remove(self, background_name:str, quiet=False) -> None:
    "Removes a background from the handler by name."
    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      background_name = background.get_name()
  
    if not self.has(background_name):
      return
    
    self.char.tags.remove(background_name, category=self.tag_category)

    if not quiet:
      self.char.msg(f"Background has been loss: {background.name}")

    if background.traits:
      for trait_name in background.traits:
        self.char.traits.remove(trait_name)

    if (invalid_backgrounds := self.validate()):
      for background_name in invalid_backgrounds:
        if not quiet:
          self.char.msg("Background was loss because prerequisities are not met.")
        self.remove(background_name, quiet=quiet)
  
  def has(self, background_name: str) -> bool:
    "Returns True if the name is found in backgrounds otherwise False."
    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      background_name = background.get_name()

    return self.char.tags.has(background_name, category=self.tag_category)

  def all(self) -> list[str]:
    "Returns a list of background names, if any."
    return self.char.tags.get(category=self.tag_category, return_list=True)
  
  def get_all(self, category: Background.Category=None):    
    results = {}
    for name in self.all():
      if background := find_background(name):
        if category and background.category != category:
          continue
        results[name] = background

    return results

  def clear(self) -> None:
    "Clears all backgrounds from the handler."
    self.char.tags.clear(category=self.tag_category)
  
  def validate(self):
    "validates the prerequisities of all backgrounds are still met."

    invalid_backgrounds = []
    for background_name in self.all():
      if not (background := find_background(background_name)):
        self.char.tags.remove(background_name, category=self.tag_category)
      elif not background.check_prerequisities(self.char, quiet=True):
        invalid_backgrounds.append(background_name)
    return invalid_backgrounds