"Elemental backgrounds"

from shinobi.backgrounds.backgrounds import Background


class BoilAffinity(Background):
  """
  You possess the affinity for the boil element, this is the the result of combining the water and fire elements.
  """

  name = "Boil Affinity"
  category = Background.Category.Elemental  

  prerequisities = {
    "elements": (True, {"water": 50, "fire": 50}),
    "stats": (True, {"cp": 20})
  }


class ExplosionAffinity(Background):
  """
  You possess the affinity for the explosion element, this is the the result of combining the earth and lightning elements.
  """

  name = "Explosion Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"earth": 50, "lightning": 50}),
    "stats": (True, {"cp": 20})
  }


class MagnetAffinity(Background):
  """
  You possess the affinity for the magnet element, this is the the result of combining the wind and earth elements.
  """

  name = "Magnet Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"wind": 50, "earth": 50}),
    "stats": (True, {"cp": 20})
  }


class IceAffinity(Background):
  """
  You possess the affinity for the ice element, this is the the result of combining the water and wind elements.
  """

  name = "Ice Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"water": 50, "wind": 50}),
    "stats": (True, {"cp": 20})
  }


class LavaAffinity(Background):
  """
  You possess the affinity for the lava element, this is the the result of combining the fire and earth elements.
  """

  name = "Lava Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"fire": 50, "earth": 50}),
    "stats": (True, {"cp": 20})
  }


class ScorchAffinity(Background):
  """
  You possess the affinity for the scorch element, this is the the result of combining the fire and water elements.
  """

  name = "Scorch Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"fire": 50, "wind": 50}),
    "stats": (True, {"cp": 20})
  }


class StormAffinity(Background):
  """
  You possess the affinity for the boil element, this is the the result of combining the lightning and water elements.
  """

  name = "Storm Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"lightning": 50, "water": 50}),
    "stats": (True, {"cp": 20})
  }


class WoodAffinity(Background):
  """
  You possess the affinity for the wood element, this is the the result of combining the earth and water elements.
  """

  name = "Wood Affinity"
  category = Background.Category.Elemental

  prerequisities = {
    "elements": (True, {"earth": 50, "water": 50}),
    "stats": (True, {"cp": 20})
  }
