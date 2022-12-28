""""""

from shinobi.modifiers.modifiers import Modifier


class _Consciousness(Modifier):
  """"""

  modifier_group = "Consciousnesses"
  modifier_id = -1

class Dead(_Consciousness):
  """"""

  modifier_id = 0

class Unconscious(_Consciousness):
  """"""

  modifier_id = 1

class Sleeping(_Consciousness):
  """"""

  modifier_id = 2

class Conscious(_Consciousness):
  """"""

  modifier_id = 3


class _Position(Modifier):
  """"""

  modifier_group = "Positions"
  modifier_id = -1

class Standing(_Position):
  """"""

  modifier_id = 0

class Sitting(_Position):
  """"""

  modifier_id = 0

class Prone(_Position):
  """"""

  modifier_id = 0
