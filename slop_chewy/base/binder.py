import collections
from typing import Dict, Union

from .formula import Formula
from .sheet import Sheet


class Binder:  # base class
    """A collection of Sheets"""
    sheet: Dict[str, Sheet]

    def __init__(self):
        self.sheet = collections.defaultdict(Sheet)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {len(self.sheet)} sheets @ 0x{id(self):016X}>"

    def __getitem__(self, sheet_name: str) -> Sheet:
        return self.sheet[sheet_name]

    def __setitem__(self, sheet_name: str, sheet: Sheet):
        self.sheet[sheet_name] = sheet

    def calculate(self, formula: Formula, sheet: Union[Sheet, str] = None) -> float:
        return formula.calculate(sheet=sheet, binder=self)
