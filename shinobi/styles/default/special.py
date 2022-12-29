"Special Styles"

from shinobi.styles.styles import Style


class AdamantineChains(Style):
  """"""

  name = "Adamantine Chains"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["uzumaki heritage"])}
  
class BodyManipulation(Style):
  """"""

  name = "Body Manipulation"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["akimichi heritage"])}
  
class ShadowManipulation(Style):
  """"""

  name = "Shadow Manipulation"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["nara heritage"])}
  
class SkeletalControl(Style):
  """"""

  name = "Skeletal Control"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["kaguya heritage"])}
  
class InsectControl(Style):
  """"""

  name = "Insect Control"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["aburame heritage"])}
  
class MindManipulation(Style):
  """"""

  name = "Mind Manipulation"
  category = Style.Category.Ninjutsu

  prerequisities = {"backgrounds": (True, ["yamanaka heritage"])}
  