from __future__ import annotations
from typing import Dict

from .. import base
from . import command


class SC(base.Binder, command.Commanded):
    """.sc file"""
    # config: ...  # store of global settings
    sheet: Dict[str, base.Sheet]
    # ^ {"name": Sheet}

    def __init__(self):
        raise NotImplementedError()

    def __repr__(self) -> str:
        raise NotImplementedError()
        # return f"<{self.__class__.__name__} len(self.sheet) sheets @ 0x{id(self):016X}>"

    @classmethod
    def from_file(cls, filepath: str) -> SC:
        raise NotImplementedError()
        out = cls()
        with open(filepath) as sc_file:
            for line in sc_file:
                out.run(line)  # Commanded method

    # TODO: command methods
    # -- group up all commands targetting a specific cell
    # -- the feed that list of commands into `sc.Cell.from_commands()`
    # --- this includes column format (width)

    # TODO: self._commands (match regex patterns to methods)
