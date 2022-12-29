"""Ninja Arts techniques"""


from shinobi.techniques.techniques import Technique


class ChakraControl(Technique):
  """
  Chakra Control determines the effectiveness when perform a technique that uses chakra.
  """

  name = "Chakra Control"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive


class ChakraFlow(Technique):
  """
  Chakra Flow determines the effectiveness when flowing chakra into other objects, including one's body.
  """

  name = "Chakra Flow"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive

  prerequisities = {"techniques": (True, {"chakra control": 20})}


class NatureTransformation(Technique):
  """
  Nature Transformation determines the effectiveness when performing a technique that uses elemental chakra.
  """

  name = "Nature Transformation"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive

  prerequisities = {"techniques": (True, {"chakra control": 20})}


class ShapeTransformation(Technique):
  """
  Shape Transformation amplies the effectiveness when performing a technique that uses chakra.
  """

  name = "Shape Transformation"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive

  prerequisities = {"techniques": (True, {"chakra control": 20})}
