"Trait modifiers"

from shinobi.modifiers.modifiers import Modifier


class _Trait(Modifier):
  """"""

  modifier_group = "Traits"
  modifier_id = -1


class Bloodline(_Trait):
  """
  The character belongs to a bloodline.
  """
  
  modifier_id = 1


class Clan(_Trait):
  """
  The character has a heritage belonging to a clan.
  """
  
  modifier_id = 2

class Orphan(_Trait):
  """
  The character has no heritage seen as an orphan.
  """
  
  modifier_id = 3