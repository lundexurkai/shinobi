"Genjutsu Styles"

from shinobi.styles.styles import Style


class Byakugan(Style):
  """
  """

  name = "Byakugan"
  category = Style.Category.Doujutsu
  prerequisities = {"backgrounds": (True, ["hyuuga heritage"])}

class Tenseigan(Style):
  """
  """

  name = "Tenseigan"
  category = Style.Category.Doujutsu
  prerequisities = {"backgrounds": (True, ["hyuuga heritage"]), "techniques": (True, {"invoke byakugan": 100})}


class Sharingan(Style):
  """
  """

  name = "Sharingan"
  category = Style.Category.Doujutsu
  prerequisities = {"backgrounds": (True, ["uchiha heritage"])}

class MangekyouSharingan(Style):
  """
  """

  name = "Mangekyou Sharingan"
  category = Style.Category.Doujutsu
  prerequisities = {"backgrounds": (True, ["uchiha heritage"]), "techniques": (True, {"invoke sharingan": 100})}
