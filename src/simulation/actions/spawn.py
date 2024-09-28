from random import randrange
from typing import Protocol, Self, override

from simulation.actions.base import Action
from simulation.entities import Entity
from simulation.exceptions import PointAlreadyUsedError
from simulation.points import Point
from simulation.world import World


class EntityFactory(Protocol):
    def spawn_entity(self) -> Entity: ...


class Spawn(Action):
    def __init__(self, count_entity: int, factory_entity: EntityFactory):
        self._count_entity = count_entity
        self._factory_entity = factory_entity

        self._spawned_entity: list[Entity] = []

    @override
    def __call__(self, world: World) -> None:
        self._spawned_entity = []

        count_spawned_entity = 0
        while count_spawned_entity < self._count_entity:
            entity = self._factory_entity.spawn_entity()
            x = randrange(0, world.width)
            y = randrange(0, world.hight)
            try:
                world.add(Point(x, y), entity)
            except PointAlreadyUsedError:
                continue

            self._spawned_entity.append(entity)

            count_spawned_entity += 1

    @override
    def undo(self, world: World) -> None:
        for entity in self._spawned_entity:
            world.remove(entity)

    def __copy__(self) -> Self:
        cls = self.__class__
        self_copy = cls(self._count_entity, self._factory_entity)
        self_copy._spawned_entity = list(self._spawned_entity)  # noqa: SLF001
        return self_copy
