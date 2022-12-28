"""
"""

from world.modifiers.modifiers import Modifier


class _Village(Modifier):
  """"""

  modifier_group = "Villages"
  modifier_id = -1


class Missing(_Village):
  modifier_id = 0

  name = "Missing"

class Leaf(_Village):
  modifier_id = 1

  name = "Leaf"

class Sand(_Village):
  modifier_id = 2

  name = "Sand"

class Mist(_Village):
  modifier_id = 3

  name = "Mist"

class Stone(_Village):
  modifier_id = 4

  name = "Stone"

class Cloud(_Village):
  modifier_id = 5

  name = "Cloud"

class _VillageRanking(Modifier):
  """"""

  modifier_group = "Rankings"
  modifier_id = -1


class Unknown(_VillageRanking):
  modifier_id = 0

  name = "Unknown"

class Citizen(_VillageRanking):
  modifier_id = 1

  name = "Citizen"

class Student(_VillageRanking):
  modifier_id = 2

  name = "Student"

class Genin(_VillageRanking):
  modifier_id = 3

  name = "Genin"

class Chuunin(_VillageRanking):
  modifier_id = 4

  name = "Chuunin"

class SpecialJounin(_VillageRanking):
  modifier_id = 5

  name = "Special Jounin"

class Jounin(_VillageRanking):
  modifier_id = 6

  name = "Jounin"

class Anbu(_VillageRanking):
  modifier_id = 7

  name = "Anbu"