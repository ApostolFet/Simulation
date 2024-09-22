from abc import ABC, abstractmethod
from random import randrange
from typing import Any, Protocol, override

from simulation.entities import Creature, Entity
from simulation.exceptions import EntityNotFoundError, PointAlreadyUsedError
from simulation.turns import Turn
from simulation.world import Point, World


class Action(ABC):
    @abstractmethod
    def __call__(self, world: World) -> None: ...


class EntityFactory(Protocol):
    def spawn_entity(self) -> Entity: ...


class SpawnAction(Action):
    def __init__(self, count_entity: int, factory_entity: EntityFactory):
        self._count_entity = count_entity
        self._factory_entity = factory_entity

    @override
    def __call__(self, world: World) -> None:
        count_spawned_entity = 0
        while count_spawned_entity < self._count_entity:
            entity = self._factory_entity.spawn_entity()
            x = randrange(0, world.width)
            y = randrange(0, world.hight)
            try:
                world.add_entity(Point(x, y), entity)
            except PointAlreadyUsedError:
                continue

            count_spawned_entity += 1


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

    def _is_execute_now(self) -> bool:
        return self._count_executed % self._interval == 0


class TurnMap:
    def __init__(self) -> None:
        self._turns_creature: dict[type[Creature], list[Turn[Any]]] = {}

    def get[T: Creature](self, creature_type: type[T]) -> list[Turn[T]]:
        return self._turns_creature.setdefault(creature_type, [])

    def add[T: Creature](self, creature_type: type[T], turns: list[Turn[T]]) -> None:
        self._turns_creature.setdefault(creature_type, []).extend(turns)


class TurnAction(Action):
    def __init__(self, turn_map: TurnMap):
        self._turn_map = turn_map

    @override
    def __call__(self, world: World) -> None:
        all_enititys = world.get_entities(Creature)
        for _, entity in all_enititys:
            if self._is_entity_dead(entity, world):
                continue

            turns = self._turn_map.get(type(entity))
            for turn in turns:
                is_turn_end = turn(entity, world)
                if is_turn_end:
                    break

    def _is_entity_dead(self, entity: Entity, world: World) -> bool:
        try:
            world.get_entity_position(entity)
        except EntityNotFoundError:
            return True

        return False
