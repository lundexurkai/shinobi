""""""

from shinobi.stats import BASIC_ELEMENTS
from shinobi.stats.elements import Element
from shinobi.stats.stathandler import StatHandler


class ElementHandler(StatHandler):

  def __init__(self, obj, attr_name="stats", attr_category="elements") -> None:
    super().__init__(obj, attr_name, attr_category)
  
  def init_defaults(self):
    for stat_key, stat_properties in BASIC_ELEMENTS.items():
      self.add(stat_key, exp=0, exp_total=0, **stat_properties)
  
  def get_all(self, category: Element.Category=None) -> dict[str, Element]:
    cache = super().get_all(type="element")

    if isinstance(category, str):
      try:
        category = Element.Category[category.title()]
      except KeyError:
        return cache

    if category is not None:
      return dict(filter(lambda i: i[1].category == category, cache.items()))
    else:
      return cache