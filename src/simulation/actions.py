from abc import ABC, abstractmethod
from copy import copy
from random import randrange
from typing import Any, Protocol, Self, override

from simulation.entities import Creature, Entity
from simulation.exceptions import EntityNotFoundError, PointAlreadyUsedError
from simulation.turns import Turn
from simulation.world import Point, World


class Action(ABC):
    @abstractmethod
    def __call__(self, world: World) -> None: ...

    @abstractmethod
    def undo(self, world: World) -> None: ...


class EntityFactory(Protocol):
    def spawn_entity(self) -> Entity: ...


class SpawnAction(Action):
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
        self._executed_turns: list[tuple[Creature, Turn[Creature]]] = []

    @override
    def __call__(self, world: World) -> None:
        self._executed_turns = []

        all_enititys = world.get_entities(Creature)
        for _, entity in all_enititys:
            if self._is_dead(entity, world):
                continue

            turns = self._turn_map.get(type(entity))
            for turn in turns:
                is_turn_end = turn(entity, world)
                self._executed_turns.append((entity, copy(turn)))
                if is_turn_end:
                    break

    @override
    def undo(self, world: World) -> None:
        for entity, turn in reversed(self._executed_turns):
            turn.undo(entity, world)
        self._executed_turns = []

    def _is_dead(self, creature: Creature, world: World) -> bool:
        if creature.hp <= 0:
            return True

        try:
            world.get_entity_position(creature)
        except EntityNotFoundError:
            return True

        return False
