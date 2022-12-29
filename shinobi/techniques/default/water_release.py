"""Water Release techniques"""


from shinobi.techniques.techniques import Technique


class TidalWave(Technique):
  """
  This technique molds chakra into a water source, sending a tidal wave toward their opponent.
  """

  name = "Tidal Wave"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant
  prerequisities = {"elements": (True, {"water": 10}), "techniques": (True, {"nature transformation": 10})}


class WaterNeedle(Technique):
  """
  This technique molds chakra into a water source, creating multiple water needles similar to senbon in size, which are tossed at the opponenet.
  """

  name = "Water Needle"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant
  prerequisities = {"elements": (True, {"water": 10}), "techniques": (True, {"nature transformation": 10})}
