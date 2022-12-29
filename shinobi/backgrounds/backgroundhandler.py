"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

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

  def __init__(self, obj: Character) -> None:
    self.obj = obj
  
  def add(self, background_name:str, quiet=False) -> None:
    """
    Adds a background to the handler by name.

    Args:
      background_name (str): the background name
      quiet (bool, optional): should it be done quietly. Defaults to False.

    Raises:
      BackgroundError: background is invalid
    """

    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
      
    background_name = background.get_name()

    if self.has(background_name):
      return
    
    self.obj.tags.add(background_name, category=self.tag_category)

    if not quiet:
      self.obj.msg(f"|CThe background |n'|w{background.name}|n'|C has been added|n.")

    if background.traits:
      for trait_name in background.traits:
        self.obj.traits.add(trait_name)

  def remove(self, background_name:str, quiet=False) -> None:
    """
    Removes a background from the handler by name.

    Args:
        background_name (str): the name of the background
        quiet (bool, optional): should it be done quietly. Defaults to False.

    Raises:
        BackgroundError: background is invalid
    """
    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
      
    background_name = background.get_name()
  
    if not self.has(background_name):
      return
    
    self.obj.tags.remove(background_name, category=self.tag_category)

    if not quiet:
      self.obj.msg(f"|RThe background |n'|w{background.name}|n'|R has been removed|n.")

    if background.traits:
      for trait_name in background.traits:
        self.obj.traits.remove(trait_name)

    if (invalid_list := self.validate()):
      for invalid in invalid_list:
        self.remove(invalid.get_name(), quiet=quiet)
  
  def has(self, background_name: str) -> bool:
    """
    Checks if the background name is found.

    Args:
        background_name (str): the name of the background

    Raises:
        BackgroundError: background is not valid

    Returns:
        bool: _description_
    """
    if not (background := find_background(background_name)):
      raise BackgroundError(f"Background not found: {background_name}")
    else:
      return self.obj.tags.has(background.get_name(), category=self.tag_category)

  def all(self) -> list[str]:
    """
    Gets a list of all background names

    Returns:
      list[str]: a list of names
    """
    return self.obj.tags.get(category=self.tag_category, return_list=True)
  
  def get_all(self, category: Background.Category=None) -> dict[str, Type[Background]]:
    """
    Gets all backgrounds from this handler as a dict.

    Args:
        category (Background.Category, optional): An optional category to sort. Defaults to None.

    Returns:
        dict[str, Type[Background]]: a dict of backgrounds
    """
    backgrounds = {name: value for name in self.all() if (value := find_background(name))}
    if category is not None:
      return dict(filter(lambda i: i[1].category == category, backgrounds.items()))
    else:
      return backgrounds

  def clear(self) -> None:
    """
    Clears all backgrounds from the handler.
    """
    for background_name in self.all():
      self.remove(background_name, quiet=True)

    self.obj.tags.clear(category=self.tag_category)
  
  def validate(self) -> list[Type[Background]]:
    """
    Validates the handler's backgrounds and returns a list of invalid.

    Returns:
        list: list of invalid backgrounds
    """

    invalid_backgrounds = []

    for background in self.get_all().values():
      if not background.check_prerequisities(self.obj, quiet=True):
        invalid_backgrounds.append(background)
    return invalid_backgrounds