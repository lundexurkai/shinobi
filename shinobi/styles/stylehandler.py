""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from shinobi.styles import find_style

if TYPE_CHECKING:
  from .styles import Style

class StyleError(RuntimeError):
  pass

class StyleHandler:

  def __init__(self, obj, attr_name="techniques", attr_category="styles") -> None:
    self.styles_data = obj.attributes.get(attr_name, category=attr_category)
    if not self.styles_data:
      obj.attributes.add(attr_name, {}, category=attr_category)
      self.styles_data = obj.attributes.get(attr_name, category=attr_category)
    
    self.obj = obj
    self._cache: dict[str, Style] = {}

  def add(self, style_name:str, force=True, quiet=False):
    if not (style := find_style(style_name)):
      raise StyleError(f"Style not found: {style_name}")
    else:
      style_name = style.get_name()

    if style_name in self.styles_data:
      if force:
        self.remove(style_name)
      else:
        raise StyleError(f"Style '{style_name}' already exists.")

    style_data = {}
    self.styles_data[style_name] = style_data

    if not quiet:
      self.obj.msg(f"|CThe technique style |n'|w{style.name}|n'|C has been added|n.")

  def get(self, style_name:str):
    style = self._cache.get(style_name)
    if not style and style_name in self.styles_data:
      if not (style_class := find_style(style_name)):
        raise StyleError(f"Style not found: {style_name}")
      style = self._cache[style_name] = style_class(self)
    return style

  def has(self, style_name: str):
    if not (style := find_style(style_name)):
      return False
    else:
      style_name = style.get_name()
    return style_name in self.styles_data.keys()

  def db(self, style_name:str):
    if style_name not in self.styles_data:
      self.styles_data[style_name] = {}
    return self.styles_data[style_name]

  def get_all(self, category:Style.Category=None) -> dict[str, Style]:
    for style_name in self.all():
      if style_name not in self._cache:
        self.get(style_name)

    styles = self._cache
    if category is not None:
      return dict(filter(lambda i: i[1].category == category, styles.items()))
    else:
      return styles

  def remove(self, style_name:str, quiet=False):
    if not (style := find_style(style_name)):
      raise StyleError(f"Style not found: {style_name}")
    else:
      style_name = style.get_name()

    if style_name not in self.styles_data:
      return
    
    if style_name in self._cache:
      del self._cache[style_name]

    del self.styles_data[style_name]

    if not quiet:
      self.obj.msg(f"|RThe technique style |n'|w{style.name}|n'|R has been removed|n.")

  def clear(self):
    for style_name in self.all():
      self.remove(style_name)

  def all(self):
    return list(self.styles_data.keys())