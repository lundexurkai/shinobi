""""""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.utils import fuzzy_search

if TYPE_CHECKING:
  from shinobi.styles.styles import Style
  from typeclasses.characters.characters import Character

  from .techniques import Technique

TECHNIQUES: dict[str, Type[Technique]] = {}

def get_all_techniques(style: Type[Style]=None) -> dict[str, Type[Technique]]:
  if style is not None:
    return {k: v for k, v in TECHNIQUES.items() if v.style == style.get_name()}
  else:
    return TECHNIQUES

def get_available_techniques(character: Character, style: Type[Style]=None) -> dict[str, Type[Technique]]:
  
  all_techniques = get_all_techniques(style)
  available_techniques: dict[str, Type[Technique]] = {}

  for technique_name, technique in all_techniques.items():
    if technique_name in character.techniques.all():
      continue
    if not character.styles.has(technique.style):
      continue
    if technique.check_prerequisities(character, quiet=True):
      available_techniques[technique_name] = technique

  return available_techniques

def find_technique(technique_name: str) -> Type[Technique] | None:
  if technique_cls := TECHNIQUES.get(technique_name):
    return technique_cls
  else:
    return fuzzy_search(technique_name, TECHNIQUES.values(), exact=True)