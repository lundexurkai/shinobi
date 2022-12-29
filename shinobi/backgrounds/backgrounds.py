""""""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from shinobi.backgrounds import find_background, find_trait
from shinobi.stats import ELEMENTS, STATS
from shinobi.utils import get_clean_name

from evennia.utils.utils import class_from_module, iter_to_str

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

  desc: str = "No description available."
  category: Category = None
  permanent = False
  prerequisities: dict[str, Any] = {}
  traits: tuple[str] = ()

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()

  @classmethod
  def get_name(cls) -> str:
    if hasattr(cls, "name"):
      name = cls.name
    else:
      name = get_clean_name(cls.__name__)
    return name.lower()
  
  @classmethod
  def check_prerequisities(cls, character: Character, quiet=False):
    "runs through the prerequisities checks"
    reasons = []

    for attr_name, args in cls.prerequisities.items():
      try:
        check_func = class_from_module(f"shinobi.prerequisities.check_{attr_name}")
      except ImportError:
        continue
      else:
        if (reason := check_func(character, *args)):
          reasons.append(reason)
    
    if reasons:
      if not quiet:
        reason_msg = "\n".join(reasons)
        character.msg(f"Unable to select background: prerequisities have not been met.\n{reason_msg}")
      return False
    else:
      return True

  @classmethod
  def get_description(cls, width, divider):
    text = ""
    text += "\n|| |c{:<24}|n: {}".format("Background Name", cls.name)
    text += "\n|| |c{:<24}|n: {}".format("Category", cls.category.name)
    text += divider

    if (blocked_backgrounds := cls.prerequisities.get("blocked_backgrounds", {})):
      endsep = ", and" if blocked_backgrounds[0] else ", or"
      backgrounds = [background for background_name in blocked_backgrounds[1] if (background := find_background(background_name))]
      backgrounds_names = iter_to_str([background.name for background in backgrounds], endsep=endsep)
    else:
      backgrounds_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Blocked backgrounds", backgrounds_names)

    if (required_backgrounds := cls.prerequisities.get("backgrounds", {})):
      endsep = ", and" if required_backgrounds[0] else ", or"
      backgrounds = [background for background_name in required_backgrounds[1] if (background := find_background(background_name))]
      backgrounds_names = iter_to_str([background.name for background in backgrounds], endsep=endsep)
    else:
      backgrounds_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required backgrounds", backgrounds_names)
  
    if (required_elements := cls.prerequisities.get("elements", {})):
      endsep = ", and" if required_elements[0] else ", or"
      elements = {k.title(): v for k, v in required_elements[1].items() if k in ELEMENTS}
      elements_names = iter_to_str(["{0} >= {1}".format(k, v) for k, v in elements.items()], endsep=endsep)
    else:
      elements_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required elements", elements_names)
  
    if cls.traits:
      traits = [trait for trait_name in cls.traits if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits])
    else:
      traits_names = "none"

    text += "\n|| |c{:<24}|n: {}".format("Added traits", traits_names)

    if (blocked_traits := cls.prerequisities.get("blocked_traits", {})):
      endsep = ", and" if blocked_traits[0] else ", or"
      traits = [trait for trait_name in blocked_traits[1] if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits], endsep=endsep)
    else:
      traits_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Blocked traits", traits_names)

    if (required_traits := cls.prerequisities.get("traits", {})):
      endsep = ", and" if required_traits[0] else ", or"
      traits = [trait for trait_name in required_traits[1] if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits], endsep=endsep)
    else:
      traits_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required traits", traits_names)

    if (required_stats := cls.prerequisities.get("stats", {})):
      endsep = ", and" if required_stats[0] else ", or"
      stats = {STATS[k]["name"]: v for k, v in required_stats[1].items()}
      stats_names = iter_to_str(["{0} >= {1}".format(k, v) for k, v in stats.items()], endsep=endsep)
    else:
      stats_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required stats", stats_names)
    text += divider

    if cls.desc:
      import textwrap
      text += "\n" + textwrap.fill(cls.desc, width = width, initial_indent="|| ", subsequent_indent="|| ")
      text += divider
    
    return text

  def __str__(self) -> str:
    return type(self).get_name()