""""""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Type

from shinobi.techniques import get_all_techniques
from shinobi.utils import get_clean_name

from evennia.utils.utils import class_from_module, lazy_property

if TYPE_CHECKING:
  from shinobi.techniques.techniques import Technique
  from typeclasses.characters.characters import Character


class Style:
  _level_descs: dict[int, str] = {}

  class Category(IntEnum):
    Doujutsu = 1
    Genjutsu = 2
    Ninjutsu = 3
    Taijutsu = 4
    Weaponry = 5

  desc = ""
  category: Style.Category = None
  permanent = False

  prerequisities: dict[str, Any] = {}

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
        character.msg(f"Unable to learn the style: prerequisities have not not been met.\n{reason_msg}")
      return False
    else:
      return True

  def __str__(self) -> str:
    return type(self).get_name()

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()

  @property
  def obj(self):
    return self.handler.obj
  
  @lazy_property
  def db(self) -> dict[str, Any]:
    return self.handler.db(self.get_name())
  
  def __init__(self, handler):
    self.handler = handler
  
  @property
  def known_techniques(self) -> dict[str, Technique]:
    return self.obj.techniques.get_all(style=self)
  
  @property
  def available_techniques(self) -> dict[str, Type[Technique]]:
    return get_all_techniques(style=self)

  @property
  def level(self) -> int: 
    out = 0
    for technique in self.known_techniques.values():
      out += technique.level
    return out

  @property
  def max_level(self) -> int: 
    out = 0
    for technique_cls in self.available_techniques.values():
      out += technique_cls.max_level
    return out
  
  @property
  def level_pct(self) -> int:
    if self.max_level == 0:
      return 0
    return round(100 * (self.level / self.max_level))
  
  @property
  def level_desc(self) -> str:
    high_desc = ""
    for bound, desc in self._level_descs.items():
      high_desc = desc
      if self.level_pct <= bound:
        return desc
    return high_desc 