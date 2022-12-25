""""""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from shinobi.utils import get_clean_name

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

class Background:

  class Category(enum.IntEnum):
    Lineage = 1
    Heritage = 2

    @property
    def title_name(self):
      return self.name.title()
    
    def __str__(self) -> str:
      return self.title_name

  desc: str = "No description available."
  category: Category = None
  prerequisities: dict[str, Any] = {}
  traits: tuple[str] = ()

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()

  @classmethod
  def _check_backgrounds_prereqs(cls, char: Character) -> str:
    "checks if the character has the required backgrounds."
    require_all, required_list = cls.prerequisities["backgrounds"]
    results = {name: char.backgrounds.has(name) for name in required_list}
    condition = all if require_all else any
    if not condition(results.values()):
      return "prerequisite background not met."
    else:
      return ""
  
  @classmethod
  def _check_traits_prereqs(cls, char: Character) -> str:
    "checks if the character has the required traits."
    require_all, required_list = cls.prerequisities["traits"]
    results = {name: char.traits.has(name) for name in required_list}
    condition = all if require_all else any
    if not condition(results.values()):
      return "prerequisite trait not met."
    else:
      return ""
  
  @classmethod
  def _check_blocked_backgrounds_prereqs(cls, char: Character) -> str:
    "checks if the character has the required backgrounds."
    required_list = cls.prerequisities["blocked_backgrounds"]
    results = {name: char.backgrounds.has(name) for name in required_list}
    if any(results.values()):
      return "prerequisite blocked background not met."
    else:
      return ""
  
  @classmethod
  def _check_blocked_traits_prereqs(cls, char: Character) -> str:
    "checks if the character has the required traits."
    required_list = cls.prerequisities["blocked_traits"]
    results = {name: char.traits.has(name) for name in required_list}
    if any(results.values()):
      return "prerequisite blocked trait not met."
    else:
      return ""

  @classmethod
  def get_name(cls) -> str:
    if hasattr(cls, "name"):
      name = cls.name
    else:
      name = get_clean_name(cls.__name__)
    return name.lower()
  
  @classmethod
  def check_prerequisities(cls, char: Character, quiet=False):
    "runs through the prerequisities checks"
    reasons = []

    for name in cls.prerequisities:
      if (func := getattr(cls, f"_check_{name}_prereqs", None)):
        if (reason := func(char)):
          reasons.append(reason)
    
    if reasons:
      if not quiet:
        pass
      return False
    else:
      return True


  def __str__(self) -> str:
    return type(self).get_name()