"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from shinobi.backgrounds.backgroundhandler import BackgroundHandler
from shinobi.backgrounds.traithandler import TraitHandler
from shinobi.modifiers.modifierhandler import ModifierHandler
from shinobi.stats.elementhandler import ElementHandler
from shinobi.stats.stathandler import StatHandler
from shinobi.styles.stylehandler import StyleHandler
from shinobi.techniques.techniquehandler import TechniqueHandler
from typeclasses.objects.objects import ObjectParent

from evennia import AttributeProperty
from evennia.contrib.game_systems.cooldowns.cooldowns import CooldownHandler
from evennia.objects.objects import DefaultCharacter
from evennia.utils.utils import lazy_property

from .handlers import PromptHandler


class Character(ObjectParent, DefaultCharacter):
  """"""

  modifier_attrs = ["consciousness", "position", "ranking", "species", "traits", "village"]

  # properties
  gender = AttributeProperty(default="neutral")
  exp = AttributeProperty(default=0)

  @lazy_property
  def backgrounds(self):
    return BackgroundHandler(self)
  
  @lazy_property
  def cooldowns(self):
    return CooldownHandler(self)

  @lazy_property
  def elements(self):
    return ElementHandler(self)

  @lazy_property
  def prompt(self):
    return PromptHandler(self)

  @lazy_property
  def stats(self):
    return StatHandler(self)

  @lazy_property
  def styles(self):
    return StyleHandler(self)

  @lazy_property
  def techniques(self):
    return TechniqueHandler(self)
  
  @lazy_property
  def traits(self):
    return TraitHandler(self)

  # modifiers
  @lazy_property
  def consciousness(self):
    return ModifierHandler(self, "consciousness", "Consciousnesses", default="conscious")
  
  @lazy_property
  def position(self):
    return ModifierHandler(self, "position", "Positions", default="standing")

  @lazy_property
  def ranking(self):
    return ModifierHandler(self, "ranking", "Rankings", default="unknown")

  @lazy_property
  def species(self):
    return ModifierHandler(self, "species", "Species", default="human")
  
  @lazy_property
  def village(self):
    return ModifierHandler(self, "village", "Villages", default="missing")

  # methods

  def at_object_creation(self):
    "Called when this character is created."
    self.elements.init_defaults()
    self.stats.init_defaults()

  def at_object_delete(self):
    "Called when this character is deleted."
    return super().at_object_delete()
