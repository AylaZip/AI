from enum import Enum, auto


class SAMapStates(Enum):
    COSTA_RICA = auto()
    PANAMA = auto()
    COLOMBIA = auto()
    VENEZUELA = auto()
    GUYANA = auto()
    SURINAME = auto()
    GUYANE = auto()
    ECUADOR = auto()
    PERU = auto()
    BRASIL = auto()
    BOLIVIA = auto()
    PARAGUAY = auto()
    CHILE = auto()
    ARGENTINA = auto()
    URUGUAY = auto()

    def __lt__(self, other):
        if type(other) != type(self):
            return False
        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))
