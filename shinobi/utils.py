""""""
import re
from typing import Any, Iterable


def get_clean_name(class_name: str):
  "Converts a class name into clean readable name."
  return " ".join(re.findall(r'[A-Z][^[A-Z]*', class_name))

def fuzzy_search(match_text: str, candidates: Iterable[Any], key=str, exact=False):
  match_text = match_text.lower()

  sorted_candidates = sorted(candidates, key=lambda candidate: len(key(candidate)))
  for candidate in sorted_candidates:
    candidate_text = key(candidate).lower()
    if match_text == candidate_text:
      return candidate
    if not exact and candidate_text.startswith(match_text):
      return candidate
