from __future__ import annotations
import collections
from typing import Dict, List, Union

from .address import CellAddress, CellRange
from .cell import Cell
from .formula import Formula


class Sheet:
    """A page of Cells"""
    # TODO: should sheets know their names for __repr__?
    cells: Dict[CellAddress, Cell]
    cursor: CellAddress
    # properties
    top_left: CellAddress
    bottom_right: CellAddress

    def __init__(self):
        self.cells = collections.defaultdict(Cell)
        self.cursor = CellAddress.from_string("A0")

    def __repr__(self) -> str:
        if self.top_left is not None:
            bounds = f"{self.top_left!s}:{self.bottom_right!s}"
        else:
            bounds = "(empty)"
        return f"<{self.__class__.__name__} {bounds} cursor={self.cursor!s} @ {id(self):016X}>"

    # TODO: isinstance(adddress, CellRange)
    def __getitem__(self, address: CellAddress) -> Cell:
        return self.cells[address]

    def __setitem__(self, address: CellAddress, cell: Cell):
        if isinstance(address, str):
            if ":" in address:  # CellRange
                raise NotImplementedError()
            address = CellAddress.from_string(address)
        if cell is None:  # clear cell
            raise NotImplementedError("Yet to decide on an implementation")
            # clear cell?
            # - self.cells[address] = Cell()
            # clear cell text & number, but keep all data intact?
        if isinstance(cell, Cell):
            self.cells[address] = cell
        elif isinstance(cell, str):
            # TODO: check if text is a formula
            self.cells[address].text = cell
        elif isinstance(cell, (int, float)):
            self.cells[address].number = cell

    def __delitem__(self, address: CellAddress):
        self.cells.pop(address)

    # APPEND / EXTEND
    def append_cell(self, cell: Cell):
        self.cells[self.cursor] = Cell
        self.cursor.column += 1

    def append_row(self, row: List[Cell]):
        start_column = self.cursor.column
        for cell in row:
            self.append_cell(cell)
        self.cursor.column = start_column
        self.cursor.row += 1

    def extend_rows(self, rows: List[List[Cell]]):
        for row in rows:
            self.append_row(row)

    # UTILITIES
    def calculate(self, formula: Formula) -> float:
        return formula.calculate(sheet=self)

    def raw_data(self, selection: CellRange = None) -> List[List[Union[str, int, None]]]:
        if selection is None:
            selection = CellRange(self.top_left, self.bottom_right)
        out = list()
        for row in selection:
            out.append(list())
            for address in row:
                cell = self.cells.get(address, None)
                if cell is None or cell.is_empty:
                    cell_value = None
                elif cell.is_text_only:
                    cell_value = cell.text
                elif cell.has_formula:
                    cell_value = self.calculate(cell.formula)
                else:  # is_number_only
                    cell_value = cell.number
                out[-1].append(cell_value)
        return out

    def sort(self, selection: CellRange, sort_function):
        raise NotImplementedError()
        # NOTE: will look at SC sort strings in future
        # -- <column><txt/num><asc/desc>

        # isolate selection
        # determine new order w/ sort_function(row)
        # delete selection from self.cells
        # re-write selection in new order

    # PROPERTIES
    @property
    def top_left(self) -> CellAddress:
        if len(self.cells) == 0:
            return None
        columns = {address.column for address in self.cells}
        column = sorted(columns)[0]
        rows = {address.row for address in self.cells}
        row = sorted(rows)[0]
        return CellAddress(column, row)

    @property
    def bottom_right(self) -> CellAddress:
        if len(self.cells) == 0:
            return None
        columns = {address.column for address in self.cells}
        column = sorted(columns)[-1]
        rows = {address.row for address in self.cells}
        row = sorted(rows)[-1]
        return CellAddress(column, row)
