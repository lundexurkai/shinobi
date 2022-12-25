"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from world.traits import find_trait

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

class TraitError(RuntimeError):
  "Trait error"
  pass

class TraitHandler:
  """
  This class handles keep track of all the known traits.
  """

  tag_category = "traits"

  def __init__(self, char: Character) -> None:
    self.char = char
  
  def add(self, trait_name:str):
    "Adds a trait to handler by name."
    if not (trait := find_trait(trait_name)):
      raise TraitError(f"Trait not found: {trait_name}")
    else:
      trait_name = trait.get_name()

    if not self.has(trait_name):
      self.char.tags.add(trait_name, category=self.tag_category)

  def remove(self, trait_name:str):
    "Removes a trait from the handler by name."
    if not (trait := find_trait(trait_name)):
      raise TraitError(f"Trait not found: {trait_name}")
    else:
      trait_name = trait.get_name()

    if self.has(trait_name):
      self.char.tags.remove(trait_name, category=self.tag_category)

  def has(self, trait_name: str) -> bool:
    "Returns True if the name is found in traits otherwise False."
    if not (trait := find_trait(trait_name)):
      raise TraitError(f"Trait not found: {trait_name}")
    else:
      trait_name = trait.get_name()

    return self.char.tags.has(trait_name, category=self.tag_category)

  def all(self):
    "Returns a list of trait names, if any."
    return self.char.tags.get(category=self.tag_category, return_list=True)

  def clear(self):
    "Clears all traits from the handler."
    self.char.tags.clear(category=self.tag_category)
