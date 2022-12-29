"Genjutsu Styles"

from shinobi.styles.styles import Style


class IllusionArts(Style):
  """
  """

  name = "Illusion Arts"
  category = Style.Category.Genjutsu
  prerequisities = {}


class SoundArts(Style):
  """
  """

  name = "Sound Arts"
  category = Style.Category.Genjutsu
  prerequisities = {"styles": (True, ["illusion arts"])}

