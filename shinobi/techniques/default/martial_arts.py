"""Martial Arts techniques"""


from shinobi.techniques.techniques import Technique


class Conditioning(Technique):
  """
  This technique increases the effectiveness when using stamina when performing techniques. It also helps reduce the amount damage recieved when enduring an attack.
  """

  name = "Conditioning"
  category = Technique.Category.Taijutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive


class Punch(Technique):
  """
  The technique deals damage to a single target, the user attempts to strike a target with a punch.
  """

  name = "Punch"
  category = Technique.Category.Taijutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Instant


class Kick(Technique):
  """
  The technique deals damage to a single target, the user attempts to strike a target with a kick.
  """

  name = "Kick"
  category = Technique.Category.Taijutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Instant


class Block(Technique):
  """
  This technique increases the chances of blocking an incoming attack, and determines how much damage is reduced upon a successful block.
  """

  name = "Block"
  category = Technique.Category.Taijutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive


class Dodge(Technique):
  """
  This technique increases the chances of dodging an incoming attack.
  """

  name = "Dodge"
  category = Technique.Category.Taijutsu
  ranking = Technique.Ranking.E
  activation = Technique.Activation.Passive
