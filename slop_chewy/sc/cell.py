import re
from typing import Callable, Dict, List

from .. import base
from ..base.cell import Alignment


class Cell(base.Cell):
    text: str
    number: float
    alignment: Alignment

    @classmethod
    def from_commands(cls, *commands: List[str]):
        out = cls()
        for command in commands:
            out.run(command)

    def as_commands(self, *config: List[str]) -> List[str]:
        raise NotImplementedError()

    # utilities
    def align(self, alignment: Alignment):
        self.alignment = alignment

    # command methods
    def leftstring(self, text: str):
        self.text = text
        self.align(Alignment.LEFT)

    # NOTE: commands could be indentified by name, but regex can capture args & verify input
    # NOTE: _commands has to defined AFTER command methods
    _commands: Dict[re.Pattern, Callable[[str], None]] = {
        r'leftstring [A-Z]+[0-9]+ = "(.*)"': leftstring}
    # leftstring A0 = "BspClass"
    # ^ {r"line regex pattern": Cell.method}
    _commands = {
        re.compile(pattern): method
        for pattern, method in _commands.items()}
