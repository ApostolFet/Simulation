from abc import ABC, abstractmethod

from simulation.world import World


class Action(ABC):
    @abstractmethod
    def __call__(self, world: World) -> None: ...

    @abstractmethod
    def undo(self, world: World) -> None: ...
