"Taijutsu Styles"

from shinobi.styles.styles import Style


class MartialArts(Style):
  """
  """

  name = "Martial Arts"
  category = Style.Category.Taijutsu
  prerequisities = {}

class Boxing(Style):
  """
  """

  name = "Boxing"
  category = Style.Category.Taijutsu
  prerequisities = {"styles": (True, ["martial arts"])}

class GentleFist(Style):
  """
  """

  name = "Gentle Fist"
  category = Style.Category.Taijutsu
  prerequisities = {"styles": (True, ["martial arts"])}

class StrongFist(Style):
  """
  """

  name = "Strong Fist"
  category = Style.Category.Taijutsu
  prerequisities = {"styles": (True, ["martial arts"])}

class Wrestling(Style):
  """
  """

  name = "Wrestling"
  category = Style.Category.Taijutsu
  prerequisities = {"styles": (True, ["martial arts"])}
