"""Fire Release techniques"""


from shinobi.techniques.techniques import Technique


class Firebolt(Technique):
  """
  This technique molds chakra into the hands converting it into heat, before pointing the hands at the opponent releasing a small bolt of fire.
  """

  name = "Firebolt"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant
  prerequisities = {"elements": (True, {"fire": 10}), "techniques": (True, {"nature transformation": 10})}


class Inferno(Technique):
  """
  This technique molds chakra into the throat and hands, releasing oxygen from the lungs into the hands which combusts into a stream of fire.
  """

  name = "Inferno"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant
  prerequisities = {"elements": (True, {"fire": 10}), "techniques": (True, {"nature transformation": 10})}


class GreatFireball(Technique):
  """
  The technique molds chakra into the throat and hands, releasing oxygen from the lungs into the hands which combusts into a fireball.
  """

  name = "Great Fireball"
  category = Technique.Category.Ninjutsu
  ranking = Technique.Ranking.C
  activation = Technique.Activation.Instant
  prerequisities = {"elements": (True, {"fire": 10}), "techniques": (True, {"nature transformation": 10})}
