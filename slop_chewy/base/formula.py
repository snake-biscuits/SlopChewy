from __future__ import annotations
import math
from typing import List

# NOTE: no type hints for Binder, Cell & Sheet classes
# from .address import CellAddress


class Formula:
    # TODO: how do we store a formula?
    # -- "@min(A1, 0)" -> {"@min": (CellAddress("A1"), 0)}
    # -- {operator: (, {function_name: CellAddress})}
    # NOTE: all function arguments should be floats
    _operators = {
        "*": float.__mul__,
        "+": lambda a, b: math.fsum([a, b])}
    # ^ {"token": function}
    # TODO: all operators
    # TODO: unary "-" operator
    _functions = {
        "min": min,
        "max": max}
    # ^ {"function_name": Function}
    # TODO: all commonplace functions
    # NOTE: sc.formula.Formula can implement functions unique to .sc
    # -- this will require sc.Cell.FormulaClass = sc.Formula
    # -- (Cell.FormulaClass isn't a thing, but it'd make sense for specialising)
    # TODO: "SheetName!Address" is valid in .xlsx, but not .sc
    # -- should have a per-class bool to check if they're legal

    def __init__(self):
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} @ 0x{id(self):016X}>"
        # return f"{self.__class__.__name__}.from_string({self!s})"

    def __str__(self) -> str:
        raise NotImplementedError()
        # TODO: construct from however we store the formula internally

    @classmethod
    def from_string(cls, formula_string: str) -> Formula:
        raise NotImplementedError()
        # TODO: tokenise w/ regex
        # -- pair w/ token type?

    @classmethod
    def from_tokens(cls, *tokens: List[str]) -> Formula:
        raise NotImplementedError()
        # TODO: create a LALR parser
        # -- "A1" -> (None, CellAddress("A1"))
        # -- "SomeSheet!C3" -> ("SomeSheet", CellAddress("C3"))
        # -- "A1:C3" -> (None, CellRange("A1", "C3"))

    def calculate(self, sheet=None, binder=None) -> float:
        # NOTE: no type hints because of circular imports
        # -- sheet: Union[Sheet, str], binder: Binder
        raise NotImplementedError()
        # NOTE: the binder is best used for formulae which index multiple sheets
        # NOTE: a binder and no sheet is valid,
        # -- but all CellAddresses must be linked to sheet names
        if sheet is None:
            # NOTE: this is ok, so long at the formula doesn't contain CellAddresses
            # TODO: verify there are no CellAddresses
            # -- CellAddresses w/ sheet names are OK if we have a binder
            ...
        if binder is None:
            if isinstance(sheet, str):
                raise RuntimeError("sheet name is useless without a binder")
        else:
            if isinstance(sheet, str):
                sheet = binder[sheet]

        # NOTE: we will need to calculate the formulae in indexed cells (if they have them):
        # -- indexed_cell_value = cell.number
        # -- if indexed_cell.has_formula:
        # --     indexed_cell_value = cell_value.calculate(indexed_sheet)
        # NOTE: caching cell values could be a neat optimisation
        # -- but this would require monitoring updates to indexed cells
        # -- which adds a lot of engineering complexity
        # -- alternatively, users w/ performance issues could try baking each cell's value as the go
        # -- though that would require knowing the layers of dependencies to a formula
        # TODO: we need a way to check for circular formula indexing
        # -- e.g. A1:"=A2+A3"; A2:"=A3"; A3: "=A1+A2";
        # -- and a way to report that to users so they can fix their formulae
