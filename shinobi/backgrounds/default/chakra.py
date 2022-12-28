"Chakra backgrounds"

from shinobi.backgrounds.backgrounds import Background


class NullChakra(Background):
  """
  A form of non-activating chakra, a condition in which a person is incapable of molding chakra as its stiff and unresponsive.
  """
  
  name = "Null Chakra"
  category = Background.Category.Chakra
  
  prerequisities = {
    "backgrounds": (True, ("orphaned heritage",))
  }