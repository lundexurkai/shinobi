""""""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from shinobi.utils import get_clean_name
from world.backgrounds import find_background
from world.traits import find_trait

from evennia.utils.utils import iter_to_str

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

class Background:

  class Category(enum.IntEnum):
    Chakra = 1
    Elemental = 2
    Heritage = 3
    Lineage = 4
    Professional = 5
    Village = 6

    @property
    def title_name(self):
      return self.name.title()
    
    def __str__(self) -> str:
      return self.title_name

  desc: str = "No description available."
  category: Category = None
  permanent = False
  prerequisities: dict[str, Any] = {}
  traits: tuple[str] = ()

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()

  @classmethod
  def _check_backgrounds_prereqs(cls, character: Character) -> str:
    "checks if the character has the required backgrounds."
    require_all, required_names = cls.prerequisities["backgrounds"]
    results = {name: character.backgrounds.has(name) for name in required_names}
    condition = all if require_all else any
    if not condition(results.values()):
      missing_backgrounds = [k for k, result in results.items() if not result]
      background_names = [background.name for name in missing_backgrounds if (background := find_background(name))]
      return "prerequisite backgrounds not met: {}".format(iter_to_str(background_names))
  
  @classmethod
  def _check_elements_prereqs(cls, character: Character) -> str:
    "checks if the character's elements mets the required elements."
    required_all, required_dict = cls.prerequisities["elements"]
    results = {element.name: element.base >= v for k, v in required_dict.items() if (element := character.elements.get(k))}
    condition = all if required_all else any
    if not condition(results.values()):
      element_names = [element_name for element_name, result in results.items() if not result]
      return "prerequisite elements not met: {}".format(iter_to_str(element_names))

  @classmethod
  def _check_stats_prereqs(cls, character: Character) -> str:
    "checks if the character's stats mets the required stats."
    required_all, required_dict = cls.prerequisities["stats"]
    results = {stat.name: stat.base >= v for k, v in required_dict.items() if (stat := character.stats.get(k))}
    condition = all if required_all else any
    if not condition(results.values()):
      stat_names = [stat_name for stat_name, result in results.items() if not result]
      return "prerequisite stats not met: {}".format(iter_to_str(stat_names))

  @classmethod
  def _check_traits_prereqs(cls, character: Character) -> str:
    "checks if the character has the required traits."
    require_all, required_names = cls.prerequisities["traits"]
    results = {name: character.traits.has(name) for name in required_names}
    condition = all if require_all else any
    if not condition(results.values()):
      missing_traits = [k for k, v in results.items() if not v]
      trait_names = [trait.get_name() for name in missing_traits if (trait := find_trait(name))]
      return "prerequisite traits not met: {}".format(iter_to_str(trait_names))
  
  @classmethod
  def _check_blocked_backgrounds_prereqs(cls, character: Character) -> str:
    "checks if the character has the required backgrounds."
    blocked_names = cls.prerequisities["blocked_backgrounds"]
    results = {name: character.backgrounds.has(name) for name in blocked_names}
    if any(results.values()):
      missing_backgrounds = [name for name, value in results.items() if not value]
      background_names = [background.name for name in missing_backgrounds if (background := find_background(name))]
      return "blocked backgrounds found: {}".format(iter_to_str(background_names))
  
  @classmethod
  def _check_blocked_traits_prereqs(cls, character: Character) -> str:
    "checks if the character has the required traits."
    blocked_names = cls.prerequisities["blocked_traits"]
    results = {name: character.traits.has(name) for name in blocked_names}
    if any(results.values()):
      missing_traits = [k for k, v in results.items() if not v]
      trait_names = [trait.get_name() for name in missing_traits if (trait := find_trait(name))]
      return "blocked traits found: {}".format(iter_to_str(trait_names))

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
        reason_msg = "\n".join(reasons)
        char.msg(f"Background prerequisities not met: {reason_msg}")
      return False
    else:
      return True


  def __str__(self) -> str:
    return type(self).get_name()