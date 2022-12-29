"""Illusion Arts techniques"""


from shinobi.techniques.techniques import Technique


class Kai(Technique):
  """
  A technique that attempts to break an illusion on the caster or a target.
  """

  name = "Genjutsu: Kai"
  category = Technique.Category.Genjutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Instant
