""""""

from shinobi.utils import get_clean_name

from evennia.utils.utils import lazy_property


class IModifiable:

  modifier_attrs: list[str] = []

  def get_all_modifiers(self):
    for attr_name in self.modifier_attrs:
      if handler := getattr(self, attr_name, None):
        for mod in handler.all():
          yield mod


class Modifier:
  """"""

  modifier_id = -1
  modifier_group = ""

  @classmethod
  def get_name(cls) -> str:
    if hasattr(cls, "name"):
      name = cls.name
    else:
      name = get_clean_name(cls.__name__)
    return name.lower()
  
  @property
  def obj(self):
    return self.handler.obj

  def __init__(self, handler) -> None:
    self.handler = handler
  
  def __str__(self) -> str:
    return type(self).get_name()

  def __int__(self):
    return self.modifier_id

  def __repr__(self):
    return "<{}: {}>".format(str(self), int(self))

  def stat_bonus(self, obj, stat_name) -> int:
    return 0

  def stat_multiplier(self, obj, stat_name) -> float:
    return 0.0
  

class ModifierSaverDict(Modifier):
  "Mixin for modifiers that can be saved."

  @lazy_property
  def db(self):
    if self.handler.save_by_id:
      flag = self.modifier_id
    else:
      flag = self.get_name()
    return self.handler.db(flag)