"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.modifiers import MODIFIERS_NAMES
from shinobi.utils import fuzzy_search

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

  from .backgrounds import Background

BACKGROUNDS: dict[str, Type[Background]] = {}


def get_all_backgrounds(category: Background.Category=None) -> dict[str, Type[Background]]:
  "Gets all backgrounds with a optional category sorter."
  if category is not None:
    return {k: v for k, v in BACKGROUNDS.items() if v.category == category}
  else:
    return dict(BACKGROUNDS)

def get_available_backgrounds(char: Character, category: Background.Category=None) -> dict[str, Type[Background]]:
  "Gets all backgrounds with prerequisities met with an optional category sorter."

  backgrounds = get_all_backgrounds(category)
  results: dict[str, Type[Background]] = {}

  for background_name, background in backgrounds.items():
    if not char.backgrounds.has(background_name) and background.check_prerequisities(char, quiet=True):
      results[background_name] = background
  
  return results

def find_background(background_name: str) -> Type[Background] | None:
  if (background := BACKGROUNDS.get(background_name)):
    return background
  else:
    return fuzzy_search(background_name, BACKGROUNDS.values(), exact=True)

def find_trait(trait_name: str) -> Type[Background] | None:
  traits = MODIFIERS_NAMES["Traits"]
  if (trait := traits.get(trait_name)):
    return trait
  else:
    return fuzzy_search(trait_name, traits.values(), exact=True)
