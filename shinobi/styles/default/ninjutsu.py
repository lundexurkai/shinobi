"Ninjutsu Styles"

from shinobi.styles.styles import Style


class NinjaArts(Style):
  """
  """

  name = "Ninja Arts"
  category = Style.Category.Ninjutsu
  prerequisities = {}

class MedicalArts(Style):
  """
  """

  name = "Medical Arts"
  category = Style.Category.Ninjutsu
  prerequisities = {"techniques": (True, {"chakra control": 20})}



class FireRelease(Style):
  """
  """

  name = "Fire Release"
  category = Style.Category.Ninjutsu
  prerequisities = {"elements": (True, {"fire": 10}), "techniques": (True, {"nature transformation": 20})}

class WindRelease(Style):
  """
  """

  name = "Wind Release"
  category = Style.Category.Ninjutsu
  prerequisities = {"elements": (True, {"wind": 10}), "techniques": (True, {"nature transformation": 20})}

class LightningRelease(Style):
  """
  """

  name = "Lightning Release"
  category = Style.Category.Ninjutsu
  prerequisities = {"elements": (True, {"lightning": 10}), "techniques": (True, {"nature transformation": 20})}

class EarthRelease(Style):
  """
  """

  name = "Earth Release"
  category = Style.Category.Ninjutsu
  prerequisities = {"elements": (True, {"earth": 10}), "techniques": (True, {"nature transformation": 20})}

class WaterRelease(Style):
  """
  """

  name = "Water Release"
  category = Style.Category.Ninjutsu
  prerequisities = {"elements": (True, {"water": 10}), "techniques": (True, {"nature transformation": 20})}


class BoilRelease(Style):
  """"""

  name = "Boil Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["boil affinity"])}

class ExplosionRelease(Style):
  """"""

  name = "Explosion Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["explosion affinity"])}

class IceRelease(Style):
  """"""

  name = "Ice Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["ice affinity"])}

class LavaRelease(Style):
  """"""

  name = "Lava Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["lava affinity"])}

class MagnetRelease(Style):
  """"""

  name = "Magnet Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["magnet affinity"])}

class ScorchRelease(Style):
  """"""

  name = "Scorch Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["scorch affinity"])}

class StormRelease(Style):
  """"""

  name = "Storm Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["storm affinity"])}

class WoodRelease(Style):
  """"""

  name = "Wood Release"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["wood affinity"])}
