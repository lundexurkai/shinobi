"Professional backgrounds"

from shinobi.backgrounds.backgrounds import Background


class FledglingCraftsman(Background):
  """ """

  name = "Fledgling Craftsman"
  category = Background.Category.Professional

  prerequisities = {
    "stats": (True, {"cp": 10}),
  }


class ApprenticeCraftsman(Background):
  """ """

  name = "Apprentice Craftsman"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["fledgling craftsman"]),
    "stats": (True, {"cp": 10}),
  }


class NoviceCraftsman(Background):
  """ """

  name = "Novice Craftsman"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["apprentice craftsman"]),
    "stats": (True, {"cp": 10}),
  }


class AccomplisedCraftsman(Background):
  """ """

  name = "Accomplised Craftsman"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["novice craftsman"]),
    "stats": (True, {"cp": 10}),
  }


class MasterCraftsman(Background):
  """ """

  name = "Master Craftsman"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["accomplised craftsman"]),
    "stats": (True, {"cp": 10}),
  }


# medical ninjutsu


class MedicalTrainee(Background):
  """ """

  name = "Medical Trainee"
  category = Background.Category.Professional

  prerequisities = {
    "stats": (True, {"cp": 10}),
  }


class MedicalAdept(Background):
  """ """

  name = "Medical Adept"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["medical trainee"]),
    "stats": (True, {"cp": 10}),
  }


class MedicalJourneyman(Background):
  """ """

  name = "Medical Journeyman"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["medical adept"]),
    "stats": (True, {"cp": 10}),
  }


class MedicalNinja(Background):
  """ """

  name = "Medical Ninja"
  category = Background.Category.Professional

  prerequisities = {
    "backgrounds": (True, ["medical journeyman"]),
    "stats": (True, {"cp": 10}),
  }