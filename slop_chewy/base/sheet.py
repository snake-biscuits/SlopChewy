from __future__ import annotations
import collections
from typing import Dict

from .address import CellAddress, CellRange
from .cell import Cell


class Sheet:
    """A page of Cells"""
    # TODO: should sheets know their names for __repr__?
    cells: Dict[CellAddress, Cell]

    def __init__(self):
        self.cells = collections.defaultdict(Cell)

    def __getitem__(self, address: CellAddress) -> Cell:
        return self.cells[address]

    def __setitem__(self, address: CellAddress, cell: Cell):
        # TODO: if cell is empty: remove it from self.cells
        self.cells[address] = cell

    def __delitem__(self, address: CellAddress):
        self.cells.pop(address)

    # TODO: more methods

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
