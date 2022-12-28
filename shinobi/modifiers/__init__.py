"""
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, Type

from shinobi.utils import fuzzy_search

if TYPE_CHECKING:
  from .modifiers import Modifier

MODIFIERS_IDS: DefaultDict[str, dict[int, Type[Modifier]]] = defaultdict(dict)
MODIFIERS_NAMES: DefaultDict[str, dict[str, Type[Modifier]]] = defaultdict(dict)


def find_modifier_class(flag: int | str, group: str):
  if isinstance(flag, int):
    if (modifiers := MODIFIERS_IDS.get(group, None)):
      if (modifier := modifiers.get(flag, None)):
        return modifier
  else:
    if (modifiers := MODIFIERS_NAMES.get(group, None)):
      if (modifier := modifiers.get(flag, None)):
        return modifier
      if (modifier_name := fuzzy_search(flag, modifiers)):
        return modifiers[modifier_name]
