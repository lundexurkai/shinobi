"""
"""


from shinobi.modifiers.modifierhandler import ModifierListHandler


class TraitHandler(ModifierListHandler):

  def __init__(self, obj) -> None:
    super().__init__(obj, attr_name="traits", group="Traits", save_by_id=False)
  
  def add(self, flag: int | str, strict=False, quiet=False):
    """
    Adds a trait to the handler

    Args:
        flag (int | str): The flag used to get trait
        strict (bool, optional): should raise an error. Defaults to False.
        quiet (bool, optional): should be done quietly. Defaults to False.
    """

    if (trait := super().add(flag, strict)):
      if not quiet:
        self.obj.msg(f"|CThe trait |n'|w{trait.get_name()}|n'|C has been added|n.")
      return trait

  def remove(self, flag: int | str, strict=False, quiet=False):
    """
    Adds a trait to the handler

    Args:
        flag (int | str): The flag used to get trait
        strict (bool, optional): should raise an error. Defaults to False.
        quiet (bool, optional): should be done quietly. Defaults to False.
    """
    
    if (trait := super().remove(flag, strict)):
      if not quiet:
        self.obj.msg(f"|RThe trait |n'|w{trait.get_name()}|n'|R has been removed|n.")
      return trait
