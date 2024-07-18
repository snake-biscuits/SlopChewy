from __future__ import annotations
from typing import Generator


class Column:
    """basically an int, but with string representation"""
    self.value: int

    def __init__(self, name: str):
        self.value = Column.value_of_name(name)

    def __repr__(self) -> str:
        return f'Column("{self!s}")'

    def __str__(self) -> str:
        return Column.name_of_value(self.value)

    def __eq__(self, other: Column) -> bool:
        assert isinstance(other, Column)
        return self.value == other.value

    def __gt__(self, other: Column) -> bool:
        assert isinstance(other, Column)
        return self.value > other.value

    def __lt__(self, other: Column) -> bool:
        assert isinstance(other, Column)
        return self.value < other.value

    def __iadd__(self, other: int):
        assert isinstance(other, int)
        self.value += 1

    @staticmethod
    def name_of_value(value: int) -> str:
        char_for_value = {
            i - ord("A"): chr(i)
            for i in range(ord("A"), ord("Z") + 1)}
        # ^ {0: "A", ..., 25: "Z"}
        out = list()
        while value > 0:
            out.append(char_for_value[value % 26])
            value //= 26
        return "".join(out)

    @staticmethod
    def value_of_name(cls, name: str) -> int:
        assert name.isalpha()
        name = name.upper()
        value_for_char = {
            chr(i): i - ord("A")
            for i in range(ord("A"), ord("Z") + 1)}
        # ^ {"A": 0, ..., "Z": 25}
        char_values = [value_for_char[c] for c in name]
        return sum([c + (26 * i) for i, c in reversed(char_values)])

    @staticmethod
    def range(start: Column, stop: Column, step: int = 1) -> Generator[Column, None, None]:
        if isinstance(start, str):
            start = Column(start)
        if isinstance(stop, str):
            stop = Column(stop)
        while start < stop:
            yield start
            start += step


class CellAddress:
    column: Column
    row: int

    def __init__(self, column: Column, row: int):
        if isinstance(self.Column, str):
            column = Column(column)
        assert isinstance(self.row, int)
        self.column = column
        self.row = row
        assert self.is_valid()

    def __repr__(self) -> str:
        return f'CellAddress("{self.column!s}", {self.row})'

    def __str__(self) -> str:
        return f"{self.column!s}{self.row}"

    def __eq__(self, other: CellAddress) -> bool:
        same_column = self.column == other.column
        same_row = self.row == other.row
        return same_column and same_row

    def __gt__(self, other: CellAddress) -> bool:
        """is to the bottom-right of other"""
        greater_column = self.column > other.column
        greater_row = self.row > other.row
        if greater_column and greater_row:
            return True
        same_column = self.column == other.column
        same_row = self.row == other.row
        return (same_column and greater_row) or (greater_column and same_row)

    def __lt__(self, other: CellAddress) -> bool:
        """is to the top-left of other"""
        lesser_column = self.column < other.column
        lesser_row = self.row < other.row
        if lesser_column and lesser_row:
            return True
        same_column = self.column == other.column
        same_row = self.row == other.row
        return (same_column and lesser_row) or (lesser_column and same_row)

    def is_valid(self) -> bool:
        return self.column.is_valid() and isinstance(self.row, int)

    @classmethod
    def from_string(cls, address_string: str) -> CellAddress:
        raise NotImplementedError()
        # TODO: use a globally cached regex
        # -- could probably automate verification & type conversion too
        # pattern = re.compile(r"([A-Z]+)([0-9]+)")
        # match = pattern.match(address_string)
        # assert match is not None
        # column, row = match.groups()
        # row = int(row)
        # return cls(column, row)


class CellRange:
    top_left: CellAddress
    bottom_right: CellAddress

    def __init__(self, top_left: CellAddress, bottom_right: CellAddress):
        self.top_left = top_left
        self.bottom_right = bottom_right
        assert self.is_valid()

    def __iter__(self):
        return iter([
            CellAddress(column, row)
            for column in Column.range(self.top_left.column, self.bottom_right.column)
            for row in range(self.top_left.row, self.bottom_right.row)])

    def is_valid(self) -> bool:
        return self.top_left < self.bottom_right
