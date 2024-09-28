from dataclasses import dataclass
from enum import Enum, auto


class Status(Enum):
    simulate = auto()
    pause = auto()
    reverse = auto()
    quit = auto()


@dataclass
class State:
    status: Status = Status.simulate
