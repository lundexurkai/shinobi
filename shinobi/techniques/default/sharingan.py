"""Sharingan techniques"""


from shinobi.techniques.techniques import Technique


class Invoke(Technique):
  """"""

  name = "Invoke Sharingan"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive

  prerequisities = {"backgrounds": (True, ("uchiha heritage", ))}


class InsightEye1(Technique):
  """"""

  name = "Eye of Insight: I"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive
  prerequisities = {"techniques": (True, {"invoke sharingan": 100})}


class InsightEye2(Technique):
  """"""

  name = "Eye of Insight: II"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive
  prerequisities = {"techniques": (True, {"eye of insight: i": 100})}


class InsightEye3(Technique):
  """"""

  name = "Eye of Insight: III"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive
  prerequisities = {"techniques": (True, {"eye of insight: ii": 100})}


class HypnotismEye1(Technique):
  """"""

  name = "Eye of Hypnotism: I"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive
  prerequisities = {"techniques": (True, {"invoke sharingan": 100})}


class HypnotismEye2(Technique):
  """"""

  name = "Eye of Hypnotism: II"
  category = Technique.Category.Doujutsu
  ranking = Technique.Ranking.D
  activation = Technique.Activation.Passive
  prerequisities = {"techniques": (True, {"eye of hypnotism: i": 100})}
