"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from world.backgrounds import find_background

if TYPE_CHECKING:
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
  
  def add(self, background_name:str) -> None:
    "Adds a background to handler by name."

    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      background_name = background.get_name()

    if self.has(background_name):
      return
    
    self.char.tags.add(background_name, category=self.tag_category)

    if background.traits:
      for trait_name in background.traits:
        self.char.traits.add(trait_name)

  def remove(self, background_name:str) -> None:
    "Removes a background from the handler by name."
    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      background_name = background.get_name()
  
    if not self.has(background_name):
      return
    
    self.char.tags.remove(background_name, category=self.tag_category)

    if background.traits:
      for trait_name in background.traits:
        self.char.traits.remove(trait_name)

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

  def clear(self) -> None:
    "Clears all backgrounds from the handler."
    self.char.tags.clear(category=self.tag_category)