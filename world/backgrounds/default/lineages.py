"Lineages backgrounds"

from world.backgrounds.backgrounds import Background


class AsurasLinege(Background):
  """
  You are a decendant of Asura Otsutsuki, the progenitor of the Senju and Uzumaki clans.
  """

  name = "Asura's Lineage"
  category = Background.Category.Lineage
  traits = ("bloodline", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan")
  }
  

class IndrasLinege(Background):
  """
  You are a decendant of Indra Otsutsuki, the progenitor of the Uchiha clan.
  """

  name = "Indra's Lineage"
  category = Background.Category.Lineage
  traits = ("bloodline", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan")
  }
  

class HamurasLinege(Background):
  """
  You are a decendant of Hamura Otsutsuki, the progenitor of the Hyuuga clan.
  """

  name = "Hamura's Lineage"
  category = Background.Category.Lineage
  traits = ("bloodline", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan")
  }
  

class KaguyasLinege(Background):
  """
  You are a decendant of Kaguya Otsutsuki, the progenitor of the Kaguya clan.
  """

  name = "Kaguya's Lineage"
  category = Background.Category.Lineage
  traits = ("bloodline", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan")
  }
  