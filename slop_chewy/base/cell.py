import enum


class Alignment(enum.Enum):
    LEFT = 0  # default for text
    CENTER = 1
    RIGHT = 2  # default for numbers


class Cell:
    text: str
    alignment: Alignment = Alignment.LEFT
    number: float
    # TODO: date processing
    # -- datefmt: str = None

    def __init__(self, text: str = None, number: float = None):
        self.text = text
        self.number = number

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} text="{self.text}" number={self.number} @ 0x{id(self):016X}>'

    def __hash__(self):
        return hash((self.text, self.number, self.alignment))

    def is_empty(self) -> bool:
        return (self.text is None) and (self.number is None)

    def is_text_only(self) -> bool:
        return (self.text is not None) and (self.number is None)

    def is_number_only(self) -> bool:
        return (self.text is None) and (self.number is not None)
