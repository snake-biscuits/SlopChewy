from __future__ import annotations
import re
from typing import Generator, List


class Column:
    """basically an int, but with string representation"""
    value: int
    name: str = property(lambda s: str(s))

    def __init__(self, name: str):
        self.value = Column.value_of_name(name)

    def __repr__(self) -> str:
        return f'Column("{self!s}")'

    def __hash__(self):
        return hash(self.value)

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

    def __add__(self, increment: int) -> Column:
        assert isinstance(increment, int)
        new_name = Column.name_of_value(self.value + increment)
        return Column(new_name)

    def __iadd__(self, increment: int) -> Column:
        assert isinstance(increment, int)
        self.value += increment

    def is_valid(self):
        return isinstance(self.value, int)

    @staticmethod
    def name_of_value(value: int) -> str:
        digits = list()
        while True:
            high, low = value // 26, value % 26
            digits.append(low)
            if high > 26:  # next digit
                value = high - 1
            elif high == 0:  # no next digit
                break
            else:  # last digit
                digits.append(high - 1)
                break
        return "".join(chr(ord("A") + v) for v in reversed(digits))

    @staticmethod
    def value_of_name(name: str) -> int:
        assert name.isalpha()
        name = name.upper()
        digits = [
            ord(c) - ord("A")
            for c in reversed(name)]
        digits[1:] = [d + 1 for d in digits[1:]]
        # if len(digits) > 1:
        #     digits[-1] += 1  # 00 -> 10 (base26)
        return sum(v * (26 ** i) for i, v in enumerate(digits))

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
        if isinstance(column, str):
            column = Column(column)
        assert isinstance(row, int)
        self.column = column
        self.row = row
        assert self.is_valid()

    def __repr__(self) -> str:
        return f'CellAddress("{self.column!s}", {self.row})'

    def __hash__(self):
        return hash((self.column, self.row))

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
        # TODO: use a globally cached regex
        # -- could probably automate verification & type conversion too
        # pattern = re.compile(r"([A-Z]+)([0-9]+)")
        # match = pattern.match(address_string)
        match = re.match(r"([A-Z]+)([0-9]+)", address_string)
        assert match is not None, f"invalid address string: {address_string}"
        column, row = match.groups()
        column = Column(column)
        row = int(row)
        return cls(column, row)


class CellRange:
    top_left: CellAddress
    bottom_right: CellAddress

    def __init__(self, top_left: CellAddress, bottom_right: CellAddress):
        self.top_left = top_left
        self.bottom_right = bottom_right
        assert self.is_valid()

    def __iter__(self) -> List[List[CellAddress]]:
        return iter([[
            CellAddress(column, row)
            for column in Column.range(self.top_left.column, self.bottom_right.column)]
            for row in range(self.top_left.row, self.bottom_right.row)])

    def is_valid(self) -> bool:
        return self.top_left < self.bottom_right
