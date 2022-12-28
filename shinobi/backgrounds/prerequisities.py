""""""


from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.backgrounds import find_background, find_trait

if TYPE_CHECKING:
  from shinobi.backgrounds.backgrounds import Background
  from typeclasses.characters.characters import Character

def check_backgrounds(character: Character, background: Type[Background]):
  required_all, backgrounds = background.prerequisities["backgrounds"]
  results = {background: character.backgrounds.has(name) for name in backgrounds if (background := find_background(name))}
  condition = all if required_all else any
  if not condition(results.values()):
    any_str = "all" if required_all else "one"
    required_names = [background.name for background, result in results.items() if not result]
    reason = "  Required background '|w{}|n' to add this background. (requires: {})"
    return "\n".join([reason.format(required_name, any_str) for required_name in required_names])

def check_elements(character: Character, background: Type[Background]) -> str:
  "checks if the character's elements mets the required elements."
  required_all, required_dict = background.prerequisities["elements"]
  results = {element: element.base >= v for k, v in required_dict.items() if (element := character.elements.get(k))}
  condition = all if required_all else any
  if not condition(results.values()):
    any_str = "all" if required_all else "one"
    required_names = [element.name for element, result in results.items() if not result]
    reason = "  '|w{}|n' affinity isn't high enough to add this background. (requires: {})"
    return "\n".join([reason.format(required_name, any_str) for required_name in required_names])


def check_stats(character: Character, background: Type[Background]) -> str:
  "checks if the character's stats mets the required stats."
  required_all, required_dict = background.prerequisities["stats"]
  results = {stat: stat.base >= v for k, v in required_dict.items() if (stat := character.stats.get(k))}
  condition = all if required_all else any
  if not condition(results.values()):
    any_str = "all" if required_all else "one"
    required_names = [stat.name for stat, result in results.items() if not result]
    reason = "  '|w{}|n' isn't high enough to add this background. (requires: {})"
    return "\n".join([reason.format(required_name, any_str) for required_name in required_names])


def check_traits(character: Character, background: Type[Background]) -> str:
  "checks if the character has the required traits."
  required_all, required_names = background.prerequisities["traits"]
  results = {trait: character.traits.has(name) for name in required_names if (trait := find_trait(name))}
  condition = all if required_all else any
  if not condition(results.values()):
    any_str = "all" if required_all else "one"
    required_names = [trait.get_name() for trait, result in results.items() if not result]
    reason = "  Required trait '|w{}|n' to add this background. (requires: {})"
    return "\n".join([reason.format(required_name, any_str) for required_name in required_names])

def check_blocked_backgrounds(character: Character, background: Type[Background]) -> str:
  "checks if the character has the required backgrounds."
  blocked_names = background.prerequisities["blocked_backgrounds"]
  results = {background: character.backgrounds.has(name) for name in blocked_names if (background := find_background(name))}
  if any(results.values()):
    required_names = [background.name for background, result in results.items() if not result]
    reason = "  Blocked background '|w{}|n' prevents this background from being added."
    return "\n".join([reason.format(required_name) for required_name in required_names])

def check_blocked_traits(character: Character, background: Type[Background]) -> str:
  "checks if the character has the required traits."
  blocked_names = background.prerequisities["blocked_traits"]
  results = {trait: character.traits.has(name) for name in blocked_names if (trait := find_trait(name))}
  if any(results.values()):
    required_names = [trait.get_name() for trait, result in results.items() if not result]
    reason = "  Blocked trait '|w{}|n' prevents this background from being added."
    return "\n".join([reason.format(required_name) for required_name in required_names])
