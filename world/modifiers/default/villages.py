"""
"""

from world.modifiers.modifiers import Modifier


class _Village(Modifier):
  """"""

  modifier_group = "Villages"
  modifier_id = -1


class Missing(_Village):
  modifier_id = 0

class Leaf(_Village):
  modifier_id = 1

class Sand(_Village):
  modifier_id = 2

class Mist(_Village):
  modifier_id = 3

class Stone(_Village):
  modifier_id = 4

class Cloud(_Village):
  modifier_id = 5

class _VillageRanking(Modifier):
  """"""

  modifier_group = "Rankings"
  modifier_id = -1


class Citizen(_VillageRanking):
  modifier_id = 0

class Student(_VillageRanking):
  modifier_id = 1

class Genin(_VillageRanking):
  modifier_id = 2

class Chuunin(_VillageRanking):
  modifier_id = 3

class SpecialJounin(_VillageRanking):
  modifier_id = 4

class Jounin(_VillageRanking):
  modifier_id = 5

class Anbu(_VillageRanking):
  modifier_id = 6