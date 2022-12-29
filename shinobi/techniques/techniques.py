""""""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from shinobi.utils import get_clean_name

from evennia.utils.utils import class_from_module, lazy_property

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character


class Technique:

  class Activation(enum.IntEnum):
    Passive = 1
    Instant = 2
    Sustain = 3
    Continous = 4
    Triggered = 5

  class Category(enum.Flag):
    Doujutsu = enum.auto()
    Genjutsu = enum.auto()
    Ninjutsu = enum.auto()
    Fuinjutsu = enum.auto()
    Taijutsu = enum.auto()

    NinTaijutsu = Ninjutsu | Taijutsu
  
  class Range(enum.IntEnum):
    Undefined = 0
    Close = 1
    Short = 2
    Mid = 3
    Long = 4
    All = 5

    @property
    def min_range(self) -> int:
      match self:
        case Technique.Range.Close:
          min_range = 0
        case Technique.Range.Short:
          min_range = 1
        case Technique.Range.Mid:
          min_range = 3
        case Technique.Range.Long:
          min_range = 6
        case Technique.Range.All:
          min_range = 10
        case _:
          min_range = -1
      return min_range
    
    @property
    def max_range(self) -> int:
      match self:
        case Technique.Range.Close:
          max_range = 1
        case Technique.Range.Short:
          max_range = 3
        case Technique.Range.Mid:
          max_range = 5
        case Technique.Range.Long:
          max_range = 10
        case Technique.Range.All:
          max_range = -1
        case _:
          max_range = -1
      return max_range

  class Ranking(enum.IntEnum):
    Undefined = 0
    E = 1
    D = 2
    C = 3
    B = 4
    A = 5
    S = 6
  
  class Result(enum.IntEnum):
    Failure = 0
    Success = 1
  
  class Targeting(enum.IntEnum):
    NotRequired = 0
    Self = 1
    Any = 2
    Object = 3
    Character = 4
    Other = 5
    OtherCharacter = 6

  desc = ""
  style = ""
  category: Technique.Category = None
  ranking: Technique.Ranking = None

  min_level = 0
  max_level = 100

  activation: Technique.Activation = None
  activation_speed = 0

  default_cooldown = 0
  handseal_count = 0

  target: Technique.Targeting = Targeting.NotRequired
  target_max = 1
  target_range: Technique.Range = Range.Undefined

  combat_use = noncombat_use = True
  
  pool_costs: dict[str, int] = {}
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
        character.msg(f"Unable to learn the technique: prerequisities have not not been met.\n{reason_msg}")
      return False
    else:
      return True

  def __str__(self) -> str:
    return type(self).get_name()

  def __init_subclass__(cls) -> None:
    if cls.__doc__:
      cls.desc = cls.__doc__.strip()
  
  @lazy_property
  def db(self) -> dict[str, Any]:
    return self.handler.db(self.get_name())
  
  def __init__(self, handler):
    self.handler = handler
  
  @property
  def obj(self):
    return self.handler.obj
  
  @property
  def active(self) -> bool:
    if self.activation == Technique.Activation.Passive:
      return True
    else:
      return self.db["active"]
  
  @active.setter
  def active(self, value: bool):
    self.db["active"] = value
  
  @property
  def exp(self) -> int:
    return self.db["exp"]
  
  @exp.setter
  def exp(self, value: int):
    self.db["exp"] = value
  
  @property
  def level(self) -> int:
    return self.db["level"]
  
  @level.setter
  def level(self, value: int):
    self.db["level"] = value

  def check_combat_flags(self, **kwargs) -> str:
    has_combat = self.obj.attributes.has("combat_handler")
    if not self.combat_use and has_combat:
      return "  This technique can only be used outside of combat."
    elif not self.noncombat_use and not has_combat:
      return "  This technique can only be used in combat."
  
  def check_cooldown(self, **kwargs) -> str:
    time_left = self.obj.cooldown.ready(self.get_name())
    if time_left:
      return f"  This technique is still on cooldown: {time_left} seconds left."
  
  def check_pool_costs(self, **kwargs) -> str:
    results = {}
    pools = self.obj.stats.get_all(type="pool")
    for pool_name, pool_cost in self.pool_costs.items():
      if (pool := pools.get(pool_name)):
        results[pool] = pool.base >= pool_cost
    
    if not all(results.values()):
      required_names = [pool.name for pool, result in results.items() if not result]
      reason = "  You don't have enough {} to execute this technique."
      return "\n".join([reason.format(required_name) for required_name in required_names])

  use_checks = ["check_combat_flags", "check_cooldown", "check_pool_costs"]
  
  def can_use(self, quiet=False, **kwargs) -> bool:
    reasons = []

    for check in self.use_checks:
      if func := getattr(self, check, None):
        if reason := func(**kwargs):
          reasons.append(reason)
    
    if reasons:
      if not quiet:
        reason_msg = "\n".join(reasons)
        self.obj.msg(f"Unable to execute the technique:\n{reason_msg}")
      return False
    else:
      return True

  def toggle_cooldown(self):
    technique_name = self.get_name()

    if self.obj.cooldowns.ready(technique_name):
      self.obj.cooldowns.set(technique_name, self.default_cooldown)
  
  def spend_pool_costs(self):
    pools = self.obj.stats.get_all(type="pool")
    for pool_name, pool_cost in self.pool_costs.items():
      if (pool := pools.get(pool_name)):
        pool.modify(-pool_cost)

  def at_pre_use(self, **kwargs):
    pass

  def use(self, **kwargs):
    if not self.can_use(quiet=False, **kwargs):
      return
    
    if not self.at_pre_use(**kwargs) is not False:
      return

    match self.activation.name:
      case "Instant":
        result = self.execute(**kwargs)
      case "Sustain" | "Continous":
        result = self.toggle(**kwargs)
      case "Triggered":
        result = self.trigger(**kwargs)
      case _:
        return
    
    match result.name:
      case "Failure":
        pass
      case "Success":
        pass

  def execute(self, **kwargs) -> Result:
    if self.at_execute(**kwargs) is not False:
      result = Technique.Result.Success
      self.spend_pool_costs()
      self.toggle_cooldown()
    else:
      result = Technique.Result.Failure

    return result
  
  def at_execute(self, **kwargs):
    pass
  
  def trigger(self, **kwargs) -> Result:
    return Technique.Result.Success

  def toggle(self, **kwargs) -> Result:
    if self.active:
      toggle_func = self.at_deactivate
    else:
      toggle_func = self.at_activate
    
    if toggle_func(**kwargs) is not False:
      result = Technique.Result.Success
      self.active = not self.active
    else:
      result = Technique.Result.Failure

    return result
  
  def at_activate(self, **kwargs):
    pass
  
  def at_deactivate(self, **kwargs):
    pass

  