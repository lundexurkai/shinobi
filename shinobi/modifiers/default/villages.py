"""
"""

from shinobi.modifiers.modifiers import Modifier


class _Village(Modifier):
  """"""

  modifier_group = "Villages"
  modifier_id = -1

  element_bonuses = {}

  def stat_bonus(self, obj, stat_name) -> int:
    return self.element_bonuses.get(stat_name, 0)


class Missing(_Village):
  """"""

  modifier_id = 0
  name = "Missing"

class Leaf(_Village):
  """"""

  modifier_id = 1
  name = "Leaf"
  element_bonuses = {"fire": 10, "wind": 0, "water": -0}

class Sand(_Village):
  """"""

  modifier_id = 2
  name = "Sand"
  element_bonuses = {"wind": 10, "lightning": 0, "fire": -0}

class Mist(_Village):
  """"""

  modifier_id = 3
  name = "Mist"
  element_bonuses = {"water": 10, "fire": 0, "earth": -0}

class Stone(_Village):
  """"""

  modifier_id = 4
  name = "Stone"
  element_bonuses = {"earth": 10, "water": 0, "lightning": -0}

class Cloud(_Village):
  """"""

  modifier_id = 5
  name = "Cloud"
  element_bonuses = {"lightning": 10, "earth": 0, "wind": -0}

class _Ranking(Modifier):
  """"""

  modifier_group = "Rankings"
  modifier_id = -1

  stat_bonuses = {}

  def stat_bonus(self, obj, stat_name) -> int:
    return self.stat_bonuses.get(stat_name, 0)


class Unknown(_Ranking):
  """"""

  modifier_id = 0
  name = "Unknown"

class Citizen(_Ranking):
  """"""

  modifier_id = 1
  name = "Citizen"

class Student(_Ranking):
  """"""

  modifier_id = 2
  name = "Student"

class Genin(_Ranking):
  """"""

  modifier_id = 3
  name = "Genin"

class Chuunin(_Ranking):
  """"""

  modifier_id = 4
  name = "Chuunin"

class SpecialJounin(_Ranking):
  """"""

  modifier_id = 5
  name = "Special Jounin"

class Jounin(_Ranking):
  """"""

  modifier_id = 6
  name = "Jounin"

class Anbu(_Ranking):
  """"""

  modifier_id = 7
  name = "Anbu"