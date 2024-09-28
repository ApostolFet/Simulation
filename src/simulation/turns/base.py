from abc import abstractmethod
from typing import Protocol

from simulation.entities import Creature
from simulation.world import World


class Turn[T: Creature](Protocol):
    @abstractmethod
    def __call__(self, entity: T, world: World) -> bool:
        """A creature's turn.

        The turn determines whether or not the creature completes the turn.
        True - completes, False - continues
        """

    @abstractmethod
    def undo(self, entity: T, world: World) -> None: ...
