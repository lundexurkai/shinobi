"Heritages backgrounds"

from shinobi.backgrounds.backgrounds import Background


class AburameHeritage(Background):
  """
  You inherit the heritage of the Aburame clan, known for their unique characteristics. 
  """

  name = "Aburame Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan"),
    "stats": (True, {"cp": 10}),
  }

class AkimichiHeritage(Background):
  """
  You inherit the heritage of the Akimichi clan, known for their unique characteristics. 
  """

  name = "Akimichi Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan"),
    "stats": (True, {"cp": 10}),
  }

class HyuugaHeritage(Background):
  """
  You inherit the heritage of the Hyuuga clan, known for their unique characteristics. 
  """

  name = "Hyuuga Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "backgrounds": (True, ("hamura's lineage", )),
    "stats": (True, {"cp": 10}),
    "blocked_traits": ("clan", "orphan")
  }

class InuzukaHeritage(Background):
  """
  You inherit the heritage of the Inuzuka clan, known for their unique characteristics. 
  """

  name = "Inuzuka Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan"),
    "stats": (True, {"cp": 10}),
  }

class KaguyaHeritage(Background):
  """
  You inherit the heritage of the Kaguya clan, known for their unique characteristics. 
  """

  name = "Kaguya Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "backgrounds": (True, ("kaguya's lineage", )),
    "stats": (True, {"cp": 10}),
    "blocked_traits": ("clan", "orphan")
  }

class NaraHeritage(Background):
  """
  You inherit the heritage of the Nara clan, known for their unique characteristics. 
  """

  name = "Nara Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan"),
    "stats": (True, {"cp": 10}),
  }


class SenjuHeritage(Background):
  """
  You inherit the heritage of the Senju clan, known for their unique characteristics. 
  """

  name = "Senju Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "backgrounds": (True, ("asura's lineage", )),
    "stats": (True, {"cp": 10}),
    "blocked_traits": ("clan", "orphan")
  }

class UzumakiHeritage(Background):
  """
  You inherit the heritage of the Uzumaki clan, known for their unique characteristics. 
  """

  name = "Uzumaki Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "backgrounds": (True, ("asura's lineage", )),
    "stats": (True, {"cp": 10}),
    "blocked_traits": ("clan", "orphan")
  }

class UchihaHeritage(Background):
  """
  You inherit the heritage of the Uchiha clan, known for their unique characteristics. 
  """

  name = "Uchiha Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "backgrounds": (True, ("indra's lineage", )),
    "stats": (True, {"cp": 10}),
    "blocked_traits": ("clan", "orphan")
  }

class YamanakaHeritage(Background):
  """
  You inherit the heritage of the Yamanaka clan, known for their unique characteristics. 
  """

  name = "Yamanaka Heritage"
  category = Background.Category.Heritage
  traits = ("clan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "orphan"),
    "stats": (True, {"cp": 10}),
  }


class OrphanedHeritage(Background):
  """
  Your heritage comes from the Orphaned 
  """

  name = "Orphaned Heritage"
  category = Background.Category.Heritage
  traits = ("orphan", )
  
  prerequisities = {
    "blocked_traits": ("bloodline", "clan"),
  }