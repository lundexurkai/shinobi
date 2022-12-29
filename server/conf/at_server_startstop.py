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

import os

from evennia.utils import logger


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """

    from django.conf import settings
    from shinobi.backgrounds import BACKGROUNDS
    from shinobi.backgrounds.backgrounds import Background
    from shinobi.modifiers import MODIFIERS_IDS, MODIFIERS_NAMES
    from shinobi.modifiers.modifiers import Modifier
    from shinobi.styles import STYLES
    from shinobi.styles.styles import Style
    from shinobi.techniques import TECHNIQUES
    from shinobi.techniques.techniques import Technique

    from evennia.utils.utils import (all_from_module, callables_from_module,
                                     inherits_from)
    
    variables = all_from_module(settings.MODIFIERS_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Modifier):
          MODIFIERS_NAMES[cls.modifier_group][cls.get_name()] = cls
          if cls.modifier_id != -1:
            MODIFIERS_IDS[cls.modifier_group][cls.modifier_id] = cls

    all_groups = list(MODIFIERS_IDS.keys())
    all_groups.extend(group for group in MODIFIERS_NAMES.keys() if group not in all_groups)

    for group in all_groups:
      num_ids = len(MODIFIERS_IDS[group])
      num_names = len(MODIFIERS_NAMES[group])
      logger.log_info(f"{group} modifiers found. [{num_ids} ids, {num_names} names]")

    variables = all_from_module(settings.BACKGROUNDS_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Background):
          BACKGROUNDS[cls.get_name()] = cls

    logger.log_info("{} total backgrounds found.".format(len(BACKGROUNDS)))

    variables = all_from_module(settings.STYLES_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Style):
          STYLES[cls.get_name()] = cls
    
    logger.log_info("{} total styles found.".format(len(STYLES)))
  
    variables = all_from_module(settings.TECHNIQUES_MODULE)
    for path in variables.get("modules", []):
      for cls in callables_from_module(path).values():
        if inherits_from(cls, Technique):
          cls.style = os.path.basename(path)[:-3].replace("_", " ")
          TECHNIQUES[cls.get_name()] = cls

    
    logger.log_info("{} total techniques found.".format(len(TECHNIQUES)))
  


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
