"""
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.utils import fuzzy_search

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

  from .traits import Trait

TRAITS: dict[str, Type[Trait]] = {}


def get_all_traits() -> dict[str, Type[Trait]]:
  "Gets all traits with a optional category sorter."
  return dict(TRAITS)

def find_trait(trait_name: str) -> Type[Trait] | None:
  if (trait := TRAITS.get(trait_name)):
    return trait
  else:
    return fuzzy_search(trait_name, TRAITS.values(), exact=True)