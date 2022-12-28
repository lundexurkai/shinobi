"""
"""

from shinobi.modifiers.modifierhandler import ModifierListHandler


class TraitHandler(ModifierListHandler):

  def __init__(self, obj) -> None:
    super().__init__(obj, attr_name="traits", group="Traits", save_by_id=False)
  
  def add(self, flag: int | str, strict=False, quiet=False):
    if (trait := super().add(flag, strict)):
      if not quiet:
        self.obj.msg(f"Trait has been added: {trait.get_name()}")

  def remove(self, flag: int | str, strict=False, quiet=False):
    if (trait := super().remove(flag, strict)):
      if not quiet:
        self.obj.msg(f"Trait has been removed: {trait.get_name()}")


class PromptHandler:

  def __init__(self, obj) -> None:
    self.obj = obj
  
  def render_stats(self):
    prompt = ""

    row_template = "|{0}{1}|n: |w{2:4.1f}|n|y%|n "
    row = ""
    pool_order = {"fat": "G", "hun": "Y", "thi": "C"}
    for stat_key, color in pool_order.items():
      if (stat := self.obj.stats.get(stat_key)):
        row += row_template.format(color, stat.name, stat.actual)

    prompt += "\n[ {} ]".format(row)
    
    row = ""
    row_template = "|{0}{1}|n: |w{2}|n [|x{3}|n] "
    pool_order = {"hp": "r", "ch": "c", "en": "y"}
    for stat_key, color in pool_order.items():
      if (stat := self.obj.stats.get(stat_key)):
        row += row_template.format(color, stat.name, stat.base, stat.actual)

    prompt += "\n[ {} ]".format(row)

    return prompt

  def get(self):
    prompt = ""
    prompt += self.render_stats()
    return prompt