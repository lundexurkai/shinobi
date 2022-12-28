"""Information commands."""

import textwrap
from collections import defaultdict
from typing import Iterable, Type

from shinobi.utils import fuzzy_search
from world.backgrounds import (find_background, get_all_backgrounds,
                               get_available_backgrounds)
from world.backgrounds.backgrounds import Background
from world.stats.stathandler import STATS
from world.traits import find_trait

from evennia import InterruptCommand
from evennia.utils.utils import iter_to_str

from .command import Command, MuxCommand


class CmdBackgrounds(MuxCommand):
  """
  show information related to backgrounds

  usage:
    backgrounds [option = [args]]
  
  switches:
    available   - shows all available backgrounds.
    details     - shows information about a background by name.
    add         - adds a background to the character, prerequisities are met.
    remove      - removes a non-permantent background.

  examples:
    backgrounds                             - shows all current backgrounds.
    backgrounds = <category>                - shows current backgrounds under a category.
    backgrounds available                   - shows all available backgrounds.
    backgrounds available = <category>      - shows all available backgrounds under a category.
    backgrounds details = <background name> - shows information about the background.
    backgrounds add = <background name>
    backgrounds remove = <background name>
  """
  
  key = "backgrounds"
  aliases = "background"
  help_category = "Information"
  options = ("available", "details", "add", "remove")

  def parse(self):
    super().parse()

    if self.lhs and self.lhs not in self.options:
      self.msg(f"Not a valid option: {self.lhs}")
      raise InterruptCommand

  def func(self):
    caller = self.caller
    categories = list(Background.Category)
    all_backgrounds = get_all_backgrounds()

    match self.lhs:
      case "add":
        if not (background_name := fuzzy_search(self.rhs, all_backgrounds.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
          return
        return self.add_background(all_backgrounds[background_name])
      case "details":
        if not (background_name := fuzzy_search(self.rhs, all_backgrounds.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
        else:
          self.show_details_background(all_backgrounds[background_name])
      case "remove":
        if not (background_name := fuzzy_search(self.rhs, all_backgrounds.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
          return
        return self.remove_background(all_backgrounds[background_name])
      case _:
        if not self.rhs:
          category = None
        else:
          if not (category := fuzzy_search(self.rhs, categories, exact=True)):
            self.msg(f"Not a valid background category: {self.rhs}")
            return
        
        if self.lhs == "available":
          self.show_available_backgrounds(category)
        else:
          self.shown_known_backgrounds(category)

    # return super().func()

  def _show_background_headers(self):
    table_headers = ("Background Name", "Req. Capacity")
    table = self.styled_table(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    table.reformat_column(0, width=60)
    table.reformat_column(1, align="l")
    table.reformat(width=self.client_width())
    
    return str(table)

  def _show_backgrounds(self, backgrounds: Iterable[Type[Background]]):
      table = self.styled_table(border="cols", align="l")

      for background in backgrounds:
        if (stats := background.prerequisities.get("stats", None)):
          required_capacity = stats[1].get("cp", 0)
        else:
          required_capacity = 0
        table.add_row(background.name, required_capacity)
      
      # format table
      table.reformat_column(0, width=60)
      table.reformat_column(1, align="l")
      table.reformat(width=self.client_width())
      
      return str(table)

  def add_background(self, background: Type[Background]): 
    
    caller = self.caller
    background_name = background.get_name()

    if caller.backgrounds.has(background_name):
      self.msg("You already have that background.")
      return

    # this handles any error msgs.
    if not background.check_prerequisities(caller, quiet=False):
      return

    # confirm background add.
    confirm = f"Are you sure you want to add the background: {background.name} yes/[no]"
    answer = ""
    answer = yield(confirm)
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Background: {background.name} has not been added.")
    else:
      caller.backgrounds.add(background_name)

  def show_details_background(self, background: Type[Background]): 
    client_width = self.client_width()
    newline_footer = "\n" + self.styled_footer()
    text = self.styled_header("Background Details:")

    text += "\n|| |c{:<24}|n: {}".format("Background Name", background.name)
    text += "\n|| |c{:<24}|n: {}".format("Category", background.category.title_name)
    text += newline_footer

    if (blocked_backgrounds := background.prerequisities.get("blocked_backgrounds", [])):
      backgrounds = [background for background_name in blocked_backgrounds if (background := find_background(background_name))]
      backgrounds_names = iter_to_str([background.name for background in backgrounds])
    else:
      backgrounds_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Blocked backgrounds", backgrounds_names)

    if (required_backgrounds := background.prerequisities.get("backgrounds", {})):
      endsep = ", and" if required_backgrounds[0] else ", or"
      backgrounds = [background for background_name in required_backgrounds[1] if (background := find_background(background_name))]
      backgrounds_names = iter_to_str([background.name for background in backgrounds], endsep=endsep)
    else:
      backgrounds_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required backgrounds", backgrounds_names)
  
    if background.traits:
      traits = [trait for trait_name in background.traits if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits])
    else:
      traits_names = "none"

    text += "\n|| |c{:<24}|n: {}".format("Added traits", traits_names)

    if (blocked_traits := background.prerequisities.get("blocked_traits", [])):
      traits = [trait for trait_name in blocked_traits if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits])
    else:
      traits_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Blocked traits", traits_names)

    if (required_traits := background.prerequisities.get("traits", {})):
      endsep = ", and" if required_traits[0] else ", or"
      traits = [trait for trait_name in required_traits[1] if (trait := find_trait(trait_name))]
      traits_names = iter_to_str([trait.get_name() for trait in traits], endsep=endsep)
    else:
      traits_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required traits", traits_names)

    if (required_stats := background.prerequisities.get("stats", {})):
      endsep = ", and" if required_stats[0] else ", or"
      stats = {STATS[k]["name"]: v for k, v in required_stats[1].items()}
      stats_names = iter_to_str(["{0} >= {1}".format(k, v) for k, v in stats.items()], endsep=endsep)
    else:
      stats_names = "none"
    
    text += "\n|| |c{:<24}|n: {}".format("Required stats", stats_names)

    text += newline_footer

    if background.desc:
      text += "\n" + textwrap.fill(background.desc, client_width, initial_indent="|| ", subsequent_indent="|| ")
      text += newline_footer

    self.msg(text)

  def remove_background(self, background: Type[Background]):
    caller = self.caller 
    background_name = background.get_name()

    if not caller.backgrounds.has(background_name):
      self.msg("You do not have that background to remove.")
      return

    if background.permanent:
      self.msg("You cannot remove permanent backgrounds.")
      return

    # confirm background remove.
    confirm_text = f"Are you sure you want to remove the background: {background.name} yes/[no]"
    answer = ""
    answer = yield(confirm_text)
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Background: {background.name} has not been removed.")
    else:
      caller.backgrounds.remove(background_name)

  def show_available_backgrounds(self, category: Background.Category=None):
    "shows known backgrounds, if category is supplied only show backgrounds of category."

    caller = self.caller    
    
    header_text = "Available Backgrounds" 
    if category is not None:
      header_text += f": {category.title_name}"

    text = self.styled_header(header_text)

    if not (available_backgrounds := get_available_backgrounds(caller, category)):
      text += "\n|| There are no backgrounds available."
    else:
      if category is not None:
        text += "\n" + self._show_backgrounds(available_backgrounds.values())
      else:
        text += "\n" + self._show_background_headers()

        categories = defaultdict(list)
        for background in available_backgrounds.values():
          categories[background.category].append(background)
        
        for category in Background.Category:
          if (backgrounds := categories[category]):
            text += "\n" + self.styled_header(category.title_name)
            text += "\n" + self._show_backgrounds(backgrounds)

    text += "\n" + self.styled_footer()
    self.msg(text)

  def shown_known_backgrounds(self, category: Background.Category=None):
    "shows known backgrounds, if category is supplied only show backgrounds of category."

    caller = self.caller
    header_text = "Backgrounds" 
    if category is not None:
      header_text += f": {category.title_name}"

    text = self.styled_header(header_text)

    if not (known_backgrounds := caller.backgrounds.get_all(category)):
      text += "\n|| You do not have any backgrounds currently."
    else:
      if category is not None:
        text += "\n" + self._show_backgrounds(known_backgrounds.values())
      else:
        text += "\n" + self._show_background_headers()
        categories = defaultdict(list)
        for background_name in known_backgrounds:
          if (background := find_background(background_name)):
            categories[background.category].append(background)
        
        for category in Background.Category:
          if (backgrounds := categories[category]):
            text += "\n" + self.styled_header(category.title_name)
            text += "\n" + self._show_backgrounds(backgrounds)

    text += "\n" + self.styled_footer()
    text += "\n|| Current traits: {}".format(iter_to_str(caller.traits.all()))
    text += "\n" + self.styled_footer()

    self.msg(text)

class CmdMissions(Command):
  """"""
  key = "missions"
  aliases = "mission"
  help_category = "Information"

  def parse(self):
    return super().parse()
  
  def func(self):
    return super().func()

class CmdSheet(Command):
  """"""
  key = "sheet"
  aliases = "score"
  help_category = "Information"

  def show_char_details(self):
    caller = self.caller
    gender = caller.gender or "neutral"

    table_data = [
      ["|cName|n", "|cRank|n"], 
      [f"|w{caller.name}|n", f"|w{caller.ranking.get().name}|n"],
      ["|cGender|n", "|cVillage|n"], 
      [f"|w{gender}|n", f"|w{caller.village.get().name}|n"],
    ]

    table = self.styled_table(border="cols", table=table_data)
    table.reformat(width=self.client_width())

    return str(table)

  
  def show_static_stats(self):
    stats = list(self.caller.stats.get_all("static").values())

    table_data, num_cols = [], 3
    for i in range(num_cols):
      data = [[], []]

      for stat in stats[i::num_cols]:
        data[0].append("|c{}|n".format(stat.name))
        data[1].append("|y{:3d}|n [|w{:3d}|n]".format(stat.actual, stat.base))
      
      table_data.extend(data)

    table = self.styled_table(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())

    return str(table)

  def show_derived_stats(self):
    stats = list(self.caller.stats.get_all("derived").values())

    table_data, num_cols = [], 3
    for i in range(num_cols):
      data = [[], []]
      for stat in stats[i::num_cols]:
        data[0].append("|c{}|n".format(stat.name))
        data[1].append("|y{:3d}|n [|w{:3d}|n]".format(stat.actual, stat.base))
      table_data.extend(data)

    table = self.styled_table(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())
    return str(table)
  
  def show_bound_stats(self):
    stats = list(self.caller.stats.get_all("bound").values())
    table_data, num_cols = [], 3
    for i in range(num_cols):
      data = [[], []]
      for stat in stats[i::num_cols]:
        data[0].append("|c{}|n".format(stat.name))
        data[1].append("|w{:3d}|n [|x{:03d}|n]".format(stat.base, stat.max))
      table_data.extend(data)

    table = self.styled_table(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())
    return str(table)
  
  def show_pool_stats(self):
    stats = list(self.caller.stats.get_all("pool").values())
    table_data, num_cols = [], 3
    for i in range(num_cols):
      data = [[], []]
      for stat in stats[i::num_cols]:
        data[0].append("|c{}|n".format(stat.name))
        data[1].append("|w{:3d}|n [|x{:03d}|n]".format(stat.base, stat.max))
      table_data.extend(data)

    table = self.styled_table(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())
    return str(table)
  
  def func(self):
    newline_footer = "\n" + self.styled_footer()
    
    text = self.styled_header("Character Sheet")
    text += "\n" + self.show_char_details()
    text += newline_footer

    text += "\n" + self.show_static_stats()
    text += newline_footer
    text += "\n" + self.show_derived_stats()
    text += newline_footer
    text += "\n" + self.show_bound_stats()
    text += newline_footer
    text += "\n" + self.show_pool_stats()
    text += newline_footer

    self.msg(text)

    # return super().func()
