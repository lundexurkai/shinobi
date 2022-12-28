""""""

BASIC_ELEMENTS = {
  "fire": {"type": "bound", "min": 0, "max": 100, "base": 0},
  "wind": {"type": "bound", "min": 0, "max": 100, "base": 0},
  "lightning": {"type": "bound", "min": 0, "max": 100, "base": 0},
  "earth": {"type": "bound", "min": 0, "max": 100, "base": 0},
  "water": {"type": "bound", "min": 0, "max": 100, "base": 0},

  "yin": {"type": "bound", "min": 0, "max": 100, "base": 0},
  "yang": {"type": "bound", "min": 0, "max": 100, "base": 0},
}


ADVANCED_ELEMENTS = {
}

ELEMENTS = BASIC_ELEMENTS | ADVANCED_ELEMENTS


from world.stats.stathandler import StatHandler


class ElementHandler(StatHandler):

  def __init__(self, obj, attr_name="stats", attr_category="elements") -> None:
    super().__init__(obj, attr_name, attr_category)
  
  def init_defaults(self):
    for element_key, element_properties in BASIC_ELEMENTS.items():
      self.add(element_key, **element_properties)