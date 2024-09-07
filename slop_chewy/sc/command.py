from __future__ import annotations
import re
from typing import Any, Callable, Dict, List


class Commanded:  # base class
    _commands: Dict[re.Pattern, Callable[(Commanded, List[Any]), None]]
    # ^ {r"command ARG": self.do_command}

    def run(self, command):
        # sanitise command
        command.rstrip()  # remove trailing whitespace
        # identify command
        for regex in self._commands:
            match = regex.match(command)
            # run command
            if match is not None:
                command_method = self._commands[regex]
                return command_method(self, *match.groups)
        else:
            raise RuntimeError(f"could not identify command: {command!r}")

    def nop(self, *args):
        """no action for this command"""
        pass
