from __future__ import annotations
import collections
from typing import Dict, List

from .address import CellAddress, CellRange
from .cell import Cell


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
        self.cursor = CellAddress("A0")

    # TODO: isinstance(adddress, CellRange)
    def __getitem__(self, address: CellAddress) -> Cell:
        return self.cells[address]

    def __setitem__(self, address: CellAddress, cell: Cell):
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

    # TODO: more methods
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

    # TODO: work on parsing formulae before revisiting this
    # -- need a way to pull a cell range
    # -- but how is it iterated over?
    # --- CellBlock class w/ __iter__ method? (should order matter?)
    # def range(self, selection: CellRange) -> Dict[CellAddress, Cell]:
    #     out = collections.defaultdict()
    #     # copy only cells with data
    #     for address in selection:
    #         if address in self.cells:
    #             out[address] = self.cells[address]
    #     return out

    def sort(self, selection: CellRange, sort_function):
        raise NotImplementedError()
        # NOTE: will look at SC sort strings in future
        # -- <column><txt/num><asc/desc>

        # isolate selection
        # determine new order w/ sort_function(row)
        # delete selection from self.cells
        # re-write selection in new order

    @property
    def top_left(self) -> CellAddress:
        out = CellAddress("A0")
        columns = {address.column for address in self.cells}
        out.column = sorted(columns)[0]
        rows = {address.row for address in self.cells}
        out.row = sorted(rows)[0]
        return out

    @property
    def bottom_right(self) -> CellAddress:
        out = CellAddress("A0")
        columns = {address.column for address in self.cells}
        out.column = sorted(columns)[-1]
        rows = {address.row for address in self.cells}
        out.row = sorted(rows)[-1]
        return out
