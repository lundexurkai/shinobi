"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_init()
at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""



from evennia.utils import logger


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """

    from django.conf import settings
    from world.backgrounds import BACKGROUNDS
    from world.backgrounds.backgrounds import Background
    from world.modifiers import MODIFIERS_IDS, MODIFIERS_NAMES
    from world.modifiers.modifiers import Modifier
    from world.traits import TRAITS
    from world.traits.traits import Trait

    from evennia.utils.utils import (all_from_module, callables_from_module,
                                     inherits_from)

    variables = all_from_module(settings.BACKGROUND_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Background):
          BACKGROUNDS[cls.get_name()] = cls
    
    logger.log_info(f"{len(BACKGROUNDS)} backgrounds loaded.")
  
    variables = all_from_module(settings.MODIFIER_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Modifier):
          MODIFIERS_NAMES[cls.modifier_group][cls.get_name()] = cls

          if cls.modifier_id != -1:
            MODIFIERS_IDS[cls.modifier_group][cls.modifier_id] = cls

    for mod_group, modifiers in MODIFIERS_IDS.items():
      logger.log_info(f"{mod_group} modifiers found: [{len(modifiers)} with ids].")
    
    for mod_group, modifiers in MODIFIERS_NAMES.items():
      logger.log_info(f"{mod_group} modifiers found: [{len(modifiers)} with names].")
  
    variables = all_from_module(settings.TRAIT_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Trait):
          TRAITS[cls.get_name()] = cls
    
    print(TRAITS)
    
    logger.log_info(f"{len(TRAITS)} traits loaded.")


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    pass


def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    pass


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
