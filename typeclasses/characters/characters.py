"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from typeclasses.objects.objects import ObjectParent
from world.backgrounds.handlers import BackgroundHandler
from world.traits.handlers import TraitHandler

from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import lazy_property


class Character(ObjectParent, DefaultCharacter):
    """"""

    # properties

    @lazy_property
    def backgrounds(self):
      return BackgroundHandler(self)
    
    @lazy_property
    def traits(self):
      return TraitHandler(self)

    # methods

    def at_object_creation(self):
        "Called when this character is created."
        return super().at_object_creation()

    def at_object_delete(self):
        "Called when this character is deleted."
        return super().at_object_delete()
