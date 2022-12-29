"""Illusion Arts techniques"""


from shinobi.techniques.techniques import Technique


class BansheeShriek(Technique):
  """
  """

  name = "Banshee Shriek"
  category = Technique.Category.Genjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant

  prerequisities = {"techniques": (True, {"chakra control": 20})}


class ParalyzingWail(Technique):
  """
  """

  name = "Paralyzing Wail"
  category = Technique.Category.Genjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant

  prerequisities = {"techniques": (True, {"chakra control": 20})}


class NumbingScream(Technique):
  """
  """

  name = "Numbing Scream"
  category = Technique.Category.Genjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant

  prerequisities = {"techniques": (True, {"chakra control": 20})}
