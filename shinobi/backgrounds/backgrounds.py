""""""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from shinobi.utils import get_clean_name

from evennia.utils.utils import class_from_module

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
      try:
        check_func = class_from_module(f"shinobi.backgrounds.prerequisities.check_{name}")
      except ImportError:
        continue
      else:
        if (reason := check_func(char, cls)):
          reasons.append(reason)
    
    if reasons:
      if not quiet:
        reason_msg = "\n".join(reasons)
        char.msg(f"Unable to add background: prerequisites have not not been met.\n{reason_msg}")
      return False
    else:
      return True

  def __str__(self) -> str:
    return type(self).get_name()