""""""


from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.backgrounds import find_background, find_trait
from shinobi.styles import find_style
from shinobi.techniques import find_technique

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character


def check_blocked_backgrounds(character: Character, required_all: bool, required_list: list):
  condition = all if required_all else any
  results = {background.name: character.backgrounds.has(req_name) for req_name in required_list if (background:= find_background(req_name))}
  if condition(results.values()):
    required_backgrounds = [background_name for background_name, result in results.items() if not result]
    reason = "The background '|W{}|n' has blocked this from happening."
    return "\n".join(reason.format(background_name) for background_name in required_backgrounds)

def check_blocked_traits(character: Character, required_all: bool, required_list: list):
  condition = all if required_all else any
  results = {trait.get_name(): character.traits.has(req_name) for req_name in required_list if (trait:= find_trait(req_name))}
  if condition(results.values()):
    required_traits = [trait_name for trait_name, result in results.items() if not result]
    reason = "The trait '|W{}|n' has blocked this from happening."
    return "\n".join(reason.format(trait_name) for trait_name in required_traits)


def check_backgrounds(character: Character, required_all: bool, required_list: list):
  condition = all if required_all else any
  results = {background.name: character.backgrounds.has(req_name) for req_name in required_list if (background:= find_background(req_name))}

  if not condition(results.values()):
    required_backgrounds = [background_name for background_name, result in results.items() if not result]
    reason = "The background '|W{}|n' is required for this to happen."
    return "\n".join(reason.format(background_name) for background_name in required_backgrounds)


def check_traits(character: Character, required_all: bool, required_list: list):
  condition = all if required_all else any
  results = {trait.get_name(): character.traits.has(req_name) for req_name in required_list if (trait:= find_trait(req_name))}

  if not condition(results.values()):
    required_traits = [trait_name for trait_name, result in results.items() if not result]
    reason = "The trait '|W{}|n' is required for this to happen."
    return "\n".join(reason.format(trait_name) for trait_name in required_traits)


def check_elements(character: Character, required_all: bool, required_dict: dict):

  def eval_condition(obj, required_base):
    return obj.base >= required_base

  condition = all if required_all else any
  results = {element.name: eval_condition(element, req_base) for req_name, req_base in required_dict.items() if (element:= character.elements.get(req_name))}

  if not condition(results.values()):
    required_elements = [element_name for element_name, result in results.items() if not result]
    reason = "Your {} affinity isn't high enough for this to happen."
    return "\n".join(reason.format(element_name) for element_name in required_elements)


def check_stats(character: Character, required_all: bool, required_dict: dict):

  def eval_condition(obj, required_base):
    return obj.base >= required_base

  condition = all if required_all else any
  results = {stat.name: eval_condition(stat, req_base) for req_name, req_base in required_dict.items() if (stat:= character.stats.get(req_name))}

  if not condition(results.values()):
    required_stats = [stat_name for stat_name, result in results.items() if not result]
    reason = "Your {} isn't high enough for this to happen."
    return "\n".join(reason.format(stat_name) for stat_name in required_stats)


def check_styles(character: Character, required_all: bool, required_list: list):
  condition = all if required_all else any
  results = {style.name: character.styles.has(req_name) for req_name in required_list if (style:= find_style(req_name))}

  if not condition(results.values()):
    required_styles = [style_name for style_name, result in results.items() if not result]
    reason = "The technique style '|W{}|n' is required for this to happen."
    return "\n".join(reason.format(style_name) for style_name in required_styles)

def check_techniques(character: Character, required_all: bool, required_dict: dict):

  def eval_condition(obj, required_level):
    # match criteria:
    #   case ">" | ">=":
    #     pass
    #   case "<" | "<=":
    #     pass
      
    return obj.level >= required_level

  condition = all if required_all else any

  results = {technique.name: character.techniques.has(req_name) for req_name in required_dict if (technique:= find_technique(req_name))}

  if not condition(results.values()):
    required_techniques = [technique_name for technique_name, result in results.items() if not result]
    reason = "The technique '|W{}|n' is required for this to happen."
    return "\n".join(reason.format(technique_name) for technique_name in required_techniques)

  results = {technique.name: eval_condition(technique, req_level) for req_name, req_level in required_dict.items() if (technique:= character.techniques.get(req_name))}

  if not condition(results.values()):
    required_techniques = [technique_name for technique_name, result in results.items() if not result]
    reason = "Your {} level isn't high enough for this to happen."
    return "\n".join(reason.format(technique_name) for technique_name in required_techniques)
