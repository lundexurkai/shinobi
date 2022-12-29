"""Character General commands."""

import textwrap
from collections import defaultdict
from typing import Iterable, Type

from shinobi.backgrounds import (find_background, find_trait,
                                 get_all_backgrounds,
                                 get_available_backgrounds)
from shinobi.backgrounds.backgrounds import Background
from shinobi.stats import STATS
from shinobi.stats.elements import Element
from shinobi.styles import find_style, get_all_styles, get_available_styles
from shinobi.styles.styles import Style
from shinobi.techniques import get_all_techniques, get_available_techniques
from shinobi.techniques.techniques import Technique
from shinobi.utils import fuzzy_search

from evennia import EvTable, InterruptCommand
from evennia.commands.cmdset import CmdSet
from evennia.utils.utils import iter_to_str

from .command import Command, MuxCommand


class CmdBackgrounds(MuxCommand):
  """
  show information related to backgrounds

  usage:
    backgrounds [option = [args]]
    backgrounds [= <category>]
  
  options:
    available [= <category>]   - shows all available backgrounds.
    details = <background>     - shows information about a background by name.
    select = <background>      - selects a background to the character.
    remove = <background>      - removes a non-permantent background.
  """
  
  key = "backgrounds"
  aliases = "background"
  help_category = "Character General"
  options = ("available", "details", "add", "remove")

  def parse(self):
    super().parse()

    if self.lhs and self.lhs not in self.options:
      self.msg(f"Not a valid option: {self.lhs}")
      raise InterruptCommand

  def func(self):

    match self.lhs:
      case "select":
        candidates = get_all_backgrounds()
        if not (background_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
        else:
          return self.select_background(candidates[background_name])
      case "details":
        candidates = get_all_backgrounds()
        if not (background_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
        else:
          self.show_background_details(candidates[background_name])
      case "remove":
        candidates = self.caller.backgrounds.get_all()
        if not (background_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No background with name found: {self.rhs}")
        else:
          return self.remove_background(candidates[background_name])
      case _:
        if self.rhs:
          candidates = list(Background.Category)
          if not (category := fuzzy_search(self.rhs, candidates, exact=True)):
            self.msg(f"Not a valid background category: {self.rhs}")
            return
        else:
          category = None

        if not self.lhs:
          self.show_known_backgrounds(category)
        else:
          self.show_available_backgrounds(category)

    # return super().func()

  def _format_table(self, table: EvTable):
    table.reformat_column(0, width=60)
    table.reformat_column(1, align="r")
    table.reformat(width=self.client_width())

  def _show_background_headers(self):
    table_headers = ("Background Name", "Req. Capacity")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_table(table)
    return str(table)

  def _show_backgrounds(self, backgrounds: Iterable[Type[Background]]):
    table = EvTable(border="cols", align="l")

    for background in backgrounds:
      if not (stats := background.prerequisities.get("stats", None)):
        req_capacity = 0
      else:
        req_capacity = stats[1].get("cp", 0)

      table.add_row(
        "|c{}|n".format(background.name),
        "|W{:03d}|n".format(req_capacity)
      )
    
    # format table
    self._format_table(table)
    return str(table)

  def _format_available_table(self, table: EvTable):
    table.reformat_column(0, width=60)
    table.reformat_column(1, align="r")
    table.reformat(width=self.client_width())

  def _show_available_background_headers(self):
    table_headers = ("Background Name", "Req. Capacity")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_table(table)
    return str(table)

  def _show_available_backgrounds(self, backgrounds: Iterable[Type[Background]]):
    table = EvTable(border="cols", align="l")

    for background in backgrounds:
      if not (stats := background.prerequisities.get("stats", None)):
        req_capacity = 0
      else:
        req_capacity = stats[1].get("cp", 0)

      table.add_row(
        "|c{}|n".format(background.name),
        "|W{:03d}|n".format(req_capacity)
      )
    
    # format table
    self._format_available_table(table)
    return str(table)

  def select_background(self, background: Type[Background]): 

    background_name = background.get_name()

    if self.caller.backgrounds.has(background_name):
      self.msg("You already have that background.")
      return

    # this handles any error msgs.
    if not background.check_prerequisities(self.caller, quiet=False):
      return

    # confirm background add.
    answer = yield(f"Are you sure you want to add the background: |w{background.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Background: {background.name} has not been added.")
    else:
      self.caller.backgrounds.add(background_name)

  def show_background_details(self, background: Type[Background]): 
    
    divider = "\n" + self.styled_footer()
    
    text = self.styled_header("Background Details:")
    text += background.get_description(width=self.client_width(), divider=divider)

    self.msg(text)

  def remove_background(self, background: Type[Background]):  
    if background.permanent:
      self.msg("You cannot remove permanent backgrounds.")
      return

    # confirm background remove.
    answer = yield(f"Are you sure you want to remove the background: |w{background.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Background: {background.name} has not been removed.")
    else:
      self.caller.backgrounds.remove(background.get_name())

  def show_available_backgrounds(self, category: Background.Category=None):
    "shows known backgrounds, if category is supplied only show backgrounds of category."

    header_text = "Available Backgrounds" 

    if category is not None:
      header_text += f": {category.name}"

    text = self.styled_header(header_text)

    available_backgrounds = list(get_available_backgrounds(self.caller, category).values())
    if not available_backgrounds:
      text += "\n|| There are no backgrounds available."
    else:
      if category is not None:
        text += "\n" + self._show_available_backgrounds(available_backgrounds)
      else:
        text += "\n" + self._show_available_background_headers()

        categories = defaultdict(list)
        for background in available_backgrounds:
          categories[background.category].append(background)
        
        for category in Background.Category:
          if (backgrounds := categories[category]):
            text += "\n" + self.styled_header(category.name)
            text += "\n" + self._show_available_backgrounds(backgrounds)

    text += "\n" + self.styled_footer()
    self.msg(text)

  def show_known_backgrounds(self, category: Background.Category=None):
    "shows known backgrounds, if category is supplied only show backgrounds of category."

    header_text = "Backgrounds" 

    if category is not None:
      header_text += f": {category.name}"

    text = self.styled_header(header_text)

    known_backgrounds = list(self.caller.backgrounds.get_all(category).values())
    if not known_backgrounds:
      text += "\n|| You do not have any backgrounds currently."
    else:
      if category is not None:
        text += "\n" + self._show_backgrounds(known_backgrounds)
      else:
        text += "\n" + self._show_background_headers()
        categories = defaultdict(list)
        for background in known_backgrounds:
          categories[background.category].append(background)
        
        for category in Background.Category:
          if not (backgrounds := categories[category]):
            continue

          text += "\n" + self.styled_header(category.name)
          text += "\n" + self._show_backgrounds(backgrounds)

    text += "\n" + self.styled_footer()
    text += "\n|| Current traits: {}".format(iter_to_str(self.caller.traits.all()))
    text += "\n" + self.styled_footer()

    self.msg(text)

class CmdElements(MuxCommand):
  """
  shows information related to affinities

  usage:
    elements
  """
  
  key = "elements"
  aliases = "element"
  help_category = "Character General"
  options = ()

  def parse(self):
    super().parse()

    if self.lhs and self.lhs not in self.options:
      self.msg(f"Not a valid option: {self.lhs}")
      raise InterruptCommand
  
  def func(self):
    match self.lhs:
      case _:
        self.show_known_elements()

  def _format_table(self, table: EvTable):
    table.reformat_column(0, align="l")
    table.reformat_column(1, width=20)
    table.reformat_column(2, width=25)
    table.reformat(width=self.client_width())

  def _show_elements(self, elements: Iterable[Element]):
    table = EvTable(border="cols", align="c")

    for element in elements:
      exp_percent = 100.0 * (element.exp / element.exp_cost)

      table.add_row(
        "|c{}|n".format(element.name), 
        "|w{}|n".format(element.rank),
        "|w{:03d}|n [ |x{:3d}|n ]".format(element.actual, element.max),
        "|w{:4.1f}|y%|n  [ |c{:3d}|n ]".format(exp_percent, element.exp_cost)
      )
    # format table
    self._format_table(table)
    
    return str(table)

  def show_known_elements(self):
    text = self.styled_header("Elements")

    elements = list(self.caller.elements.get_all().values())
    if not elements:
      text += "\n|| You do not have any elemental affinities."
    else:
      headers = ("Element", "Rank", "Affinity", "Exp % [Exp Cost]")
      table = EvTable(border="cols", align="c")
      table.add_row(*headers)
    
      self._format_table(table)
      text += "\n" + str(table)

      categories = defaultdict(list)
      for element in elements:
          categories[element.category].append(element)

      for category in Element.Category:
        if not (elements := categories[category]):
          continue
        else:
          text += "\n" + self.styled_header(category.name)
          text += "\n" + self._show_elements(elements)
    
    text += "\n" + self.styled_footer()
    self.msg(text)

class CmdMissions(Command):
  """"""
  key = "missions"
  aliases = "mission"
  help_category = "Character General"

  def parse(self):
    return super().parse()
  
  def func(self):
    return super().func()

class CmdStyles(MuxCommand):
  """
  show information about technique styles

  usage:
    styles [option = [args]]
    styles [= <category>]

  options:
    available [= <category>]       - shows all available technique styles
    details = <style>              - shows information about a style by name.
    learn = <style>                - adds a technique style to the character.
    forget = <style>               - removes a technique style from the character.
  """
  key = "styles"
  aliases = "style"
  help_category = "Character General"
  options = ("available", "details", "learn", "forget")

  def parse(self):
    super().parse()

    if self.lhs and self.lhs not in self.options:
      self.msg(f"Not a valid option: {self.lhs}")
      raise InterruptCommand
  
  def func(self):

    match self.lhs:
      case "learn":
        candidates = get_all_styles()
        if not (style_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No style with name found: {self.rhs}")
          return
        return self.learn_style(candidates[style_name])
      case "details":
        candidates = get_all_styles()
        if not (style_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No style with name found: {self.rhs}")
        else:
          self.show_style_details(candidates[style_name])
      case "forget":
        candidates = self.caller.styles.get_all()
        if not (style_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No style with name found: {self.rhs}")
          return
        return self.forget_style(candidates[style_name])
      case _:
        if self.rhs:
          categories = list(Style.Category)
          if not (category := fuzzy_search(self.rhs, categories, exact=True)):
            self.msg(f"Not a valid style category: {self.rhs}")
            return
        else:
          category = None
        
        if not self.lhs:
          self.show_known_styles(category)
        else:
          self.show_available_styles(category)
  
    # return super().func()

  def _format_table(self, table: EvTable):
    table.reformat_column(0, width=40)
    table.reformat_column(1, width=15)
    table.reformat_column(2, align="r")
    table.reformat(width=self.client_width())

  def _show_style_headers(self):
    table_headers = ("Technique Style", "Known Count", "Available Count")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_table(table)
    return str(table)

  def _show_styles(self, styles: Iterable[Style]):
    table = EvTable(border="cols", align="l")

    for style in styles:
      table.add_row(
        "|c{}|n".format(style.name),
        "|w{}|n".format(len(style.known_techniques)),
        "|w{}|n".format(len(style.available_techniques)),
      )
      
    # format table
    self._format_table(table)
    return str(table)

  def _format_available_table(self, table: EvTable):

    table.reformat_column(0, width=40)
    table.reformat_column(1, align="r")
    table.reformat(width=self.client_width())

  def _show_available_style_headers(self):
    table_headers = ("Technique Style", "Required Capacity")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_available_table(table)
    return str(table)
  
  def _show_available_styles(self, styles: Iterable[Type[Style]]):
    table = EvTable(border="cols", align="l")

    for style in styles:
      if (stats := style.prerequisities.get("stats", None)):
        required_capacity = stats[1].get("cp", 0)
      else:
        required_capacity = 0
  
      table.add_row(
        "|c{}|n".format(style.name),
        "|w{:03d}|n".format(required_capacity)
      )
      
    # format table
    self._format_available_table(table)
    return str(table)
  
  def learn_style(self, style: Type[Style]) -> None:
    style_name = style.get_name()

    if self.caller.styles.has(style_name):
      self.msg("You already have that technique style.")
      return

    # this handles any error msgs.
    if not style.check_prerequisities(self.caller, quiet=False):
      return

    # confirm style add.
    answer = yield(f"Are you sure you want to add the style: |w{style.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Style: {style.name} has not been added.")
    else:
      self.caller.styles.add(style_name)
  
  def show_style_details(self, style: Type[Style]):
    client_width = self.client_width()
    divider = "\n" + self.styled_footer()
    text = self.styled_header("Style Details:")

    text += "\n|| |c{:<24}|n: {}".format("Style Name", style.name)
    text += "\n|| |c{:<24}|n: {}".format("Category", style.category.name)

    if (stats := style.prerequisities.get("stats", None)):
      required_capacity = stats[1].get("cp", 0)
    else:
      required_capacity = 0

    text += "\n|| |c{:<24}|n: {}".format("Required Capacity", required_capacity)
    
    if style.desc:
      text += "\n" + textwrap.fill(style.desc, client_width, initial_indent="|| ", subsequent_indent="|| ")
      text += divider

    available_techniques = list(get_available_techniques(self.caller, style).values())
    if available_techniques:
      headers = ["Technique Name", "Rank", "Req. Capacity"]
      table = self.styled_table(*headers, border="cols", align="l")

      for technique in sorted(available_techniques, key=lambda t: t.ranking, reverse=True):
        if (stats := technique.prerequisities.get("stats", None)):
          required_capacity = stats[1].get("cp", 0)
        else:
          required_capacity = 0
        
        table.add_row(
            technique.name,
            technique.ranking.name,
            f"{required_capacity:<3d}",
        )

      self._format_table(table)

      text += "\n" + self.styled_header("Available Techniques")
      text += "\n" + str(table)

    text += divider
    self.msg(text)

  
  def forget_style(self, style: Type[Style]):
    if style.permanent:
      self.msg("You cannot remove permanent styles.")
      return

    # confirm style remove.
    answer = yield(f"Are you sure you want to remove the style: |w{style.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Style: {style.name} has not been removed.")
    else:
      self.caller.styles.remove(style.get_name())
  
  def show_available_styles(self, category:Style.Category=None):     
    header_text = "Available Styles" 
    
    if category is not None:
      header_text += f": {category.name}"

    text = self.styled_header(header_text)

    available_styles = list(get_available_styles(self.caller, category).values())
    if not available_styles:
      text += "\n|| There are no available technique styles."
    else:
      if category is not None:
        text += "\n" + self._show_available_styles(available_styles)
      else:
        text += "\n" + self._show_available_style_headers()

        categories = defaultdict(list)
        for style in available_styles:
          categories[style.category].append(style)
        
        for category in Style.Category:
          if not (styles := categories[category]):
            continue
          else:
            text += "\n" + self.styled_header(category.name)
            text += "\n" + self._show_available_styles(styles)

    text += "\n" + self.styled_footer()
    self.msg(text)

  def show_known_styles(self, category:Style.Category=None): 
    header_text = "Styles" 

    if category is not None:
      header_text += f": {category.name}"

    text = self.styled_header(header_text)
    known_styles = list(self.caller.styles.get_all(category).values())
    if not known_styles:
      text += "\n|| You do not have any technique styles currently."
    else:
      if category is not None:
        text += "\n" + self._show_styles(known_styles)
      else:
        text += "\n" + self._show_style_headers()
        
        categories = defaultdict(list)
        for style in known_styles:
          categories[style.category].append(style)
        
        for category in Style.Category:
          if not (styles := categories[category]):
            continue
          else:
            text += "\n" + self.styled_header(category.name)
            text += "\n" + self._show_styles(styles)

    text += "\n" + self.styled_footer()
    self.msg(text)

class CmdSheet(Command):
  """"""
  key = "sheet"
  aliases = "score"
  help_category = "Character General"

  def show_char_details(self):
    caller = self.caller
    gender = caller.gender or "neutral"

    table_data = [
      ["|cName|n", "|cRank|n"], 
      [f"|w{caller.name}|n", f"|w{caller.ranking.get().name}|n"],
      ["|cGender|n", "|cVillage|n"], 
      [f"|w{gender}|n", f"|w{caller.village.get().name}|n"],
    ]

    table = EvTable(border="cols", table=table_data)
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

    table = EvTable(border="cols", table=table_data)

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

    table = EvTable(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())
    return str(table)
  
  def show_bounded_stats(self):
    stats = list(self.caller.stats.get_all("bounded").values())
    table_data, num_cols = [], 3
    for i in range(num_cols):
      data = [[], []]
      for stat in stats[i::num_cols]:
        data[0].append("|c{}|n".format(stat.name))
        data[1].append("|w{:3d}|n [|x{:03d}|n]".format(stat.base, stat.max))
      table_data.extend(data)

    table = EvTable(border="cols", table=table_data)

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
        data[1].append("|w{:3d}|n [|x{:03d}|n]".format(stat.base, stat.actual))
      table_data.extend(data)

    table = EvTable(border="cols", table=table_data)

    for i in range(6):
      if i % 2 == 0:
        table.reformat_column(i, width=20)
      else:
        table.reformat_column(i, align="r")

    table.reformat(width=self.client_width())
    return str(table)
  
  def func(self):
    divider = "\n" + self.styled_footer()
    
    text = self.styled_header("Character Sheet")
    text += "\n" + self.show_char_details()
    text += divider

    text += "\n" + self.show_static_stats()
    text += divider
    text += "\n" + self.show_derived_stats()
    text += divider
    text += "\n" + self.show_bounded_stats()
    text += divider
    text += "\n" + self.show_pool_stats()
    text += divider

    self.msg(text)

class CmdTechniques(MuxCommand):
  """"""
  key = "techniques"
  aliases = "technique"
  help_category = "Character General"
  options = ("available", "details", "learn", "forget")

  def parse(self):
    super().parse()

    if self.lhs and self.lhs not in self.options:
      self.msg(f"Not a valid option: {self.lhs}")
      raise InterruptCommand
  
  def func(self):

    match self.lhs:
      case "learn":
        candidates = get_all_techniques()
        if not (technique_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No technique with name found: {self.rhs}")
        else:
          return self.learn_technique(candidates[technique_name])
      case "details":
        candidates = get_all_techniques()
        if not (technique_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No technique with name found: {self.rhs}")
        else:
          self.show_details_technique(candidates[technique_name])
      case "forget":
        candidates = self.caller.techniques.get_all()
        if not (technique_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
          self.msg(f"No technique with name found: {self.rhs}")
        else:
          return self.forget_technique(candidates[technique_name])
      case _:
        if self.rhs:
          if not self.lhs:
            candidates = self.caller.styles.get_all()
          else:
            candidates = get_all_styles()

          if not (style_name := fuzzy_search(self.rhs, candidates.keys(), exact=True)):
            self.msg(f"Not a valid style name: {self.rhs}")
            return
          
          style = candidates[style_name]
        else:
          style = None

        if not self.lhs:
          self.show_known_techniques(style)
        else:
          self.show_available_techniques(style)
  
    # return super().func()

  def _format_table(self, table: EvTable):
    # table.reformat_column(0, width=30)
    table.reformat_column(1, width=15)
    table.reformat_column(2, width=10)
    table.reformat(width=self.client_width())

  def _show_technique_headers(self):
    table_headers = ("Technique Name", "Category", "Ranking", "Activation")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_table(table)
    return str(table)

  def _show_techniques(self, techniques: Iterable[Technique]):
    table = EvTable(border="cols", align="l")

    for technique in techniques:
      table.add_row(
        "|c{}|n".format(technique.name),
        technique.category.name,
        technique.ranking.name,
        technique.activation.name
      )
      
    # format table
    self._format_table(table)
    return str(table)
  
  def _format_available_table(self, table: EvTable):
    table.reformat_column(0, width=50)
    table.reformat_column(1, align="r")
    table.reformat(width=self.client_width())

  def _show_available_technique_headers(self):
    table_headers = ("Technique Name", "Required Capacity")
    table = EvTable(border="cols", align="l")
    table.add_row(*table_headers)
      
    # format table
    self._format_available_table(table)
    return str(table)

  def _show_available_techniques(self, techniques: Iterable[Type[Technique]]):
    table = EvTable(border="cols", align="l")

    for technique in techniques:
      if not (stats := technique.prerequisities.get("stats", None)):
        req_capacity = 0
      else:
        req_capacity = stats[1].get("cp", 0)

      table.add_row(
        "|c{}|n".format(technique.name),
        "|W{:03d}|n".format(req_capacity)
      )
      
    # format table
    self._format_available_table(table)
    return str(table)
  
  def learn_technique(self, technique: Type[Technique]) -> None:
    
    technique_name = technique.get_name()

    if self.caller.techniques.has(technique_name):
      self.msg("You already have that technique.")
      return

    # this handles any error msgs.
    if not technique.check_prerequisities(self.caller, quiet=False):
      return

    # confirm technique add.
    answer = yield(f"Are you sure you want to add the technique: |w{technique.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Technique: {technique.name} has not been added.")
    else:
      self.caller.techniques.add(technique_name)
  
  def show_details_technique(self, technique: Type[Technique]):
    divider = "\n" + self.styled_footer()
    text = self.styled_header("Technique Details:")

    text += "\n|| |c{:<24}|n: {}".format("Technique Name", technique.name)
    text += "\n|| |c{:<24}|n: {}".format("Category", technique.category.name)
    text += divider

    # text += divider

    if technique.desc:
      text += "\n" + textwrap.fill(technique.desc, width = self.client_width(), initial_indent="|| ", subsequent_indent="|| ")
      text += divider

    self.msg(text)
  
  def forget_technique(self, technique: Type[Technique]):

    if technique.permanent:
      self.msg("You cannot remove permanent techniques.")
      return

    # confirm technique remove.
    answer = yield(f"Are you sure you want to remove the technique: |w{technique.name}|n (yes/[no])")
    answer = "no" if answer == "" else answer
    
    valid_answers = ("yes", "y", "no", "n")
    if answer and answer not in valid_answers:
      self.msg("Aborting, either accept the default by pressing enter or specify yes or no.")
    elif answer.strip().lower() in valid_answers[2:]:
      self.msg(f"Technique: {technique.name} has not been removed.")
    else:
      self.caller.techniques.remove(technique.get_name())
  
  def show_available_techniques(self, style: Type[Style]=None): 
    
    header_text = "Available Techniques" 
    
    if style is not None:
      header_text += f": {style.name}"

    text = self.styled_header(header_text)

    available_techniques = list(get_available_techniques(self.caller, style).values())
    if not available_techniques:
      text += "\n|| There are no available techniques."
    else:
      if style is not None:
        text += "\n" + self._show_available_techniques(available_techniques)
      else:
        text += "\n" + self._show_available_technique_headers()

        styles = defaultdict(list)
        for technique in available_techniques:
          if (style := find_style(technique.style)):
            styles[style.name].append(technique)

        for style_name, techniques in styles.items():
          text += "\n" + self.styled_header(style_name)
          text += "\n" + self._show_available_techniques(techniques)

    text += "\n" + self.styled_footer()
    self.msg(text)

  def show_known_techniques(self, style: Type[Style]=None):

    header_text = "Techniques" 

    if style is not None:
      header_text += f": {style.name}"

    text = self.styled_header(header_text)

    known_techniques = list(self.caller.techniques.get_all(style).values())
    if not known_techniques:
      text += "\n|| You do not have any techniques currently."
    else:
      if style is not None:
        text += "\n" + self._show_techniques(known_techniques)
      else:
        text += "\n" + self._show_technique_headers()
        
        styles = defaultdict(list)
        for technique in known_techniques:
          if (style := find_style(technique.style)):
            styles[style.name].append(technique)

        for style_name, techniques in styles.items():
          text += "\n" + self.styled_header(style_name)
          text += "\n" + self._show_techniques(techniques)

    text += "\n" + self.styled_footer()
    self.msg(text)

class CharacterGeneralCmdSet(CmdSet):
  ""

  key = "character_general"

  def at_cmdset_creation(self):
    "Populate the cmdset"
    self.add(CmdBackgrounds())
    self.add(CmdElements())
    self.add(CmdMissions())
    self.add(CmdStyles())
    self.add(CmdSheet())
    self.add(CmdTechniques())