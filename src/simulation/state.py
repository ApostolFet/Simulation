from dataclasses import dataclass
from enum import Enum, auto


class Status(Enum):
    start = auto()
    pause = auto()
    stop = auto()
    back = auto()


@dataclass
class State:
    status: Status = Status.start
