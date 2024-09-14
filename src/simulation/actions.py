from abc import ABC, abstractmethod
from random import randrange
from typing import Any, override

from simulation.entities import Creature, Entity, Grass, Herbivore, Predator, Rock, Tree
from simulation.turns import Turn
from simulation.world import Point, World


class Action(ABC):
    @abstractmethod
    def __call__(self, world: World) -> None: ...


class SpawnAction(Action):
    def __init__(self, count_entity: int):
        self._count_entity = count_entity

    @override
    def __call__(self, world: World) -> None:
        for _ in range(self._count_entity):
            entity = self.spawn_entity()
            x = randrange(0, world.width)
            y = randrange(0, world.hight)
            world.add_entity(Point(x, y), entity)

    @abstractmethod
    def spawn_entity(self) -> Entity: ...


class SpawnHerbivoreAction(SpawnAction):
    @override
    def spawn_entity(self) -> Herbivore:
        return Herbivore(hp=100, speed=2, target=Grass)


class SpawnPredatorAction(SpawnAction):
    @override
    def spawn_entity(self) -> Predator:
        return Predator(hp=100, speed=2, target=Herbivore, power=50)


class SpawnTreeAction(SpawnAction):
    @override
    def spawn_entity(self) -> Tree:
        return Tree()


class SpawnGrassAction(SpawnAction):
    @override
    def spawn_entity(self) -> Grass:
        return Grass()


class SpawnRockAction(SpawnAction):
    @override
    def spawn_entity(self) -> Rock:
        return Rock()


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
        all_enititys = world.get_all_entitys()
        for _, entity in all_enititys:
            if not isinstance(entity, Creature):
                continue

            turns = self._turn_map.get(type(entity))
            for turn in turns:
                is_turn_end = turn(entity, world)
                if is_turn_end:
                    break
