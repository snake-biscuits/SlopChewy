import collections
from typing import Dict

from . sheet import Sheet


class Binder:  # base class
    """A collection of Sheets"""
    sheet: Dict[str, Sheet]

    def __init__(self):
        self.sheet = collections.defaultdict(Sheet)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {len(self.sheet)} sheets @ 0x{id(self):016X}>"
