""""""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
  from .stats import Stat

BASIC_ELEMENTS: dict[str, dict[str, Any]] = {
  "fire": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "wind": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "lightning": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "earth": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "water": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "yin": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"},
  "yang": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "basic"}
}

ADVANCED_ELEMENTS: dict[str, dict[str, Any]] = {
  "boil": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "explosion": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "magnet": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "ice": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "lava": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "scorch": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "boil": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
  "wood": {"type": "element", "base": 0, "min": 0, "max": 100, "category": "advanced"},
}

ELEMENTS = BASIC_ELEMENTS | ADVANCED_ELEMENTS

STAT_TYPES: dict[str, Type[Stat]] = {}

STATS: dict[str, dict[str, Any]] = {
  "str": {"type": "static", "base": 1, "name": "Strength"},
  "dex": {"type": "static", "base": 1, "name": "Dexterity"},
  "end": {"type": "static", "base": 1, "name": "Endurance"},
  "int": {"type": "static", "base": 1, "name": "Intelligence"},
  "per": {"type": "static", "base": 1, "name": "Perception"},
  "wit": {"type": "static", "base": 1, "name": "Wits"},
  "spi": {"type": "static", "base": 1, "name": "Spirit"},
  "pre": {"type": "static", "base": 1, "name": "Precision"},
  "man": {"type": "static", "base": 1, "name": "Manipulation"},

  "acc": {"type": "derived", "base": 0, "name": "Accuracy"},
  "rea": {"type": "derived", "base": 0, "name": "Readiness"},

  "def": {"type": "derived", "base": 0, "name": "Deflection"},
  "for": {"type": "derived", "base": 0, "name": "Fortitude"},
  "ref": {"type": "derived", "base": 0, "name": "Reflex"},
  "wil": {"type": "derived", "base": 0, "name": "Willpower"},
  
  "hun": {"type": "bounded", "min": 0, "max": 100, "base": 100, "name": "Hunger"},
  "thi": {"type": "bounded", "min": 0, "max": 100, "base": 100, "name": "Thrist"},
  "fat": {"type": "bounded", "min": 0, "max": 100, "base": 0, "name": "Fatigue"},
  
  "hp": {"type": "pool", "max": 50, "base": 50, "name": "Health"},
  "ch": {"type": "pool", "max": 10, "base": 10, "name": "Chakra"},
  "en": {"type": "pool", "max": 100, "base": 100, "name": "Energy"},
  "cp": {"type": "pool", "max": 100, "base": 100, "name": "Capacity"},
  "re": {"type": "pool", "max": 0, "base": 0, "name": "Reserve"},
}