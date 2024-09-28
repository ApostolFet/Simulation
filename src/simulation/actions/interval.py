from copy import copy
from typing import Self, override

from simulation.actions.base import Action
from simulation.world import World


class IntervalAction(Action):
    def __init__(self, interval: int, action: Action) -> None:
        self._interval = interval
        self._action = action
        self._count_executed = 0

    @override
    def __call__(self, world: World) -> None:
        self._count_executed += 1
        if self._is_execute_now():
            self._action(world)

    @override
    def undo(self, world: World) -> None:
        if self._is_execute_now():
            self._action.undo(world)

        self._count_executed -= 1

    def _is_execute_now(self) -> bool:
        return self._count_executed % self._interval == 0

    def __copy__(self) -> Self:
        cls = self.__class__
        self_copy = cls(self._interval, copy(self._action))
        self_copy._count_executed = self._count_executed  # noqa: SLF001
        return self_copy
