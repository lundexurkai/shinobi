""""""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from shinobi.utils import fuzzy_search

if TYPE_CHECKING:
  from typeclasses.characters.characters import Character

  from .styles import Style

STYLES: dict[str, Type[Style]] = {}

def get_all_styles(category: Style.Category=None) -> dict[str, Type[Style]]:
  if category is not None:
    return {k: v for k, v in STYLES.items() if v.category == category}
  else:
    return STYLES

def get_available_styles(character: Character, category: Style.Category=None) -> dict[str, Type[Style]]:
  
  all_styles = get_all_styles(category)
  available_styles: dict[str, Type[Style]] = {}

  for style_name, style in all_styles.items():
    if style_name in character.styles.all():
      continue
    if style.check_prerequisities(character, quiet=True):
      available_styles[style_name] = style

  return available_styles

def find_style(style_name: str) -> Type[Style] | None:
  if style_cls := STYLES.get(style_name):
    return style_cls
  else:
    return fuzzy_search(style_name, STYLES.values(), exact=True)