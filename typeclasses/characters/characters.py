"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from typeclasses.objects.objects import ObjectParent
from world.backgrounds.backgroundhandler import BackgroundHandler
from world.modifiers.modifierhandler import ModifierHandler
from world.stats.stathandler import StatHandler
from world.traits.traithandler import TraitHandler

from evennia import AttributeProperty
from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import lazy_property

from .handlers import PromptHandler


class Character(ObjectParent, DefaultCharacter):
    """"""

    # properties
    gender = AttributeProperty()

    @lazy_property
    def backgrounds(self):
      return BackgroundHandler(self)
    
    @lazy_property
    def prompt(self):
      return PromptHandler(self)

    @lazy_property
    def stats(self):
      return StatHandler(self)
    
    @lazy_property
    def traits(self):
      return TraitHandler(self)

    # modifiers
    @lazy_property
    def consciousness(self):
      return ModifierHandler(self, "consciousness", "Consciousnesses")
    
    @lazy_property
    def position(self):
      return ModifierHandler(self, "position", "Positions")
  
    @lazy_property
    def species(self):
      return ModifierHandler(self, "species", "Species")

    # methods

    def at_object_creation(self):
        "Called when this character is created."
        return super().at_object_creation()

    def at_object_delete(self):
        "Called when this character is deleted."
        return super().at_object_delete()
