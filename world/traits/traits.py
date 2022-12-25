"Traits"

from shinobi.utils import get_clean_name


class Trait:
  desc = "No description available."

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

  def __str__(self) -> str:
    return type(self).get_name()
