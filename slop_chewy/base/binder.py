import collections
from typing import Dict, Union

from .formula import Formula
from .sheet import Sheet


class Binder:  # base class
    """A collection of Sheets"""
    sheets: Dict[str, Sheet]

    def __init__(self):
        self.sheets = collections.defaultdict(Sheet)

    def __repr__(self) -> str:
        descriptor = f"{len(self.sheets)} sheets"
        return f"<{self.__class__.__name__} {descriptor} @ 0x{id(self):016X}>"

    def __getitem__(self, sheet_name: str) -> Sheet:
        return self.sheets[sheet_name]

    def __setitem__(self, sheet_name: str, sheet: Sheet):
        self.sheets[sheet_name] = sheet

    def calculate(self, formula: Formula, sheet: Union[Sheet, str] = None) -> float:
        return formula.calculate(sheet=sheet, binder=self)
