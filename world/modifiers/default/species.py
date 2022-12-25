"""
"""

from world.modifiers.modifiers import Modifier


class _Species(Modifier):
  """"""

  modifier_group = "Species"
  modifier_id = -1


class Animal(_Species):

  modifier_id = 0

class Human(_Species):
  "The default option for players."

  modifier_id = 1