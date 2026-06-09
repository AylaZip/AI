from enum import Enum, auto


class States(Enum):
    CLEAN = auto()
    DIRTY = auto()
    UNKNOWN = auto()

    def __repr__(self):
        return self.name


class Action(Enum):
    SUCK = auto()
    RIGHT = auto()
    LEFT = auto()
    NO_OP = auto()

    def __repr__(self):
        return self.name


class Location(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    UNKNOWN = auto()

    def allowed_moves(self) -> tuple[Action, ...]:
        always_allowed = Action.NO_OP, Action.SUCK
        if self == Location.A:
            return Action.RIGHT, *always_allowed
        if self == Location.B:
            return Action.LEFT, Action.RIGHT, *always_allowed
        if self == Location.C:
            return Action.LEFT, Action.RIGHT, *always_allowed
        if self == Location.D:
            return Action.LEFT, *always_allowed
        return always_allowed

    def __repr__(self):
        return self.name


type LocationState = tuple[Location, States]
