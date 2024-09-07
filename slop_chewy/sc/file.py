from __future__ import annotations
import re
from typing import Any, Dict, List

from .. import base
from . import command


class SC(base.Binder, command.Commanded):
    """.sc file"""
    config: Dict[str, Any]  # store of global settings
    sheets: Dict[str, base.Sheet]
    # ^ {"name": Sheet}
    # EDITOR STATE
    current_sheet: str
    current_cell: base.CellAddress

    def __init__(self):
        super().__init__(self)
        self.config = dict()
        # default state
        self.current_sheet = "Sheet1"
        self.current_cell = base.CellAddress.from_string("A0")

    @classmethod
    def from_file(cls, filepath: str) -> SC:
        with open(filepath) as sc_file:
            return cls.from_lines(sc_file.readlines())

    @classmethod
    def from_lines(cls, lines: List[str]) -> SC:
        """run a series of commands on a blank SC"""
        out = cls()
        for line in lines:
            out.run(line)
        return out

    # COMMAND METHODS
    # TODO: group up all commands targetting a specific cell
    # -- then feed that list of commands into `sc.Cell.from_commands()`
    # --- this includes column format (width)

    def move_to_sheet(self, sheet_name: str):
        self.current_sheet = sheet_name

    # COMMANDS
    _commands = {
            # nops
            r"": command.Commanded.nop,  # blank line
            r"# .*": command.Commanded.nop,  # comment
            r"newsheet .*": command.Commanded.nop,  # unnessecary
            # not implemented
            r"format ([A-Z]+) ([0-9]+) ([0-9]+) ([0-9]+)": command.Commanded.nop,  # column format
            r"freeze [0-9]+": command.Commanded.nop,  # freeze row
            r"nb_.*": command.Commanded.nop,  # frozen state?
            r"offsrc_.*": command.Commanded.nop,  # offscreen?
            # sheet ops
            r'movetosheet "(.*)"': move_to_sheet,
            # cell ops
            # ...: ...
            }
    _commands = {
        re.compile(regex): command_func
        for regex, command_func in _commands.items()}
