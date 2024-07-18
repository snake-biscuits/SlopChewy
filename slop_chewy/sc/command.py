from __future__ import annotations
import re
from typing import Any, Callable, Dict, List


class Commanded:  # base class
    _commands: Dict[re.Pattern, Callable[(Commanded, List[Any]), None]]
    # ^ {r"command ARG": self.do_command}

    def run(self, command) -> None:
        for regex in self._commands:
            match = regex.match(command)
            if match is not None:
                command_method = self._commands[regex]
                command_method(self, *match.groups)  # do it
