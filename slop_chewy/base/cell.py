import enum
from typing import Union

from .formula import Formula


class Alignment(enum.Enum):
    LEFT = 0  # default for text
    CENTER = 1
    RIGHT = 2  # default for numbers


class Cell:
    text: str
    alignment: Alignment = Alignment.LEFT
    number: Union[float, Formula]
    # TODO: date processing
    # -- datefmt: str = None
    # properties
    is_empty: bool
    is_text_only: bool
    is_number_only: bool
    has_formula: bool

    def __init__(self, text: str = None, number: float = None):
        assert isinstance(text, str)
        self.text = text
        if isinstance(number, (int, float, type(None))):
            self.number = number
        elif isinstance(number, (str, Formula)):
            self.number = None
            if isinstance(number, Formula):
                self.number = number
            else:
                self.number = Formula.from_string(number)

    def __repr__(self) -> str:
        text = f'"{self.text}"' if self.text is not None else None
        number = f"[{self.number!s}]" if self.number is not None else None
        # NOTE: using {self.number!s} to ensure we use Formula.__str__, not __repr__
        if text is not None or number is not None:
            contents = " ".join([x for x in (text, number) if x is not None])
        else:
            contents = "(empty)"
        return f'<{self.__class__.__name__} {contents} @ 0x{id(self):016X}>'

    def __hash__(self):
        return hash((self.text, self.number, self.alignment))

    # PROPERTIES
    @property
    def has_formula(self) -> bool:
        return isinstance(self.number, Formula)

    @property
    def is_empty(self) -> bool:
        return (self.text is None) and (self.number is None)

    @property
    def is_text_only(self) -> bool:
        return (self.text is not None) and (self.number is None)

    @property
    def is_number_only(self) -> bool:
        return (self.text is None) and (self.number is not None)
