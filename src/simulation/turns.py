from abc import abstractmethod
from typing import Protocol, override

from simulation.entities import Creature, Entity, Grass, Herbivore, Predator
from simulation.world import Point, World


class FindPathStrategy(Protocol):
    def __call__(
        self,
        current_point: Point,
        target_point: Point,
        world: World,
    ) -> list[Point]: ...


class Turn[T: Creature](Protocol):
    @abstractmethod
    def __call__(self, entity: T, world: World) -> bool: ...


class Move(Turn[Creature]):
    def __init__(self, find_path_strategy: FindPathStrategy) -> None:
        self._find_path = find_path_strategy

    @override
    def __call__(self, entity: Creature, world: World) -> bool:
        current_point = world.get_entity_position(entity)
        target_entitys = world.get_entities(entity.target)
        target_point = find_closest_point_entity(
            current_point,
            target_entitys,
            entity.visual_radius,
        )
        if target_point is None:
            path = [current_point]
        else:
            path = self._find_path(current_point, target_point, world)

        if len(path) <= entity.speed:
            world.add_entity(path[-1], entity)
            return False
        world.add_entity(path[entity.speed], entity)
        return True


class Attack(Turn[Predator]):
    @override
    def __call__(self, entity: Predator, world: World) -> bool:
        target_entitys = world.get_entities(Herbivore)
        entity_point = world.get_entity_position(entity)
        closest_entity = find_near_entity(entity_point, target_entitys)
        if closest_entity is None:
            return False

        closest_entity.hp -= entity.power
        if closest_entity.hp < 0:
            world.remove_entity(closest_entity)
        return True


class Eat(Turn[Herbivore]):
    @override
    def __call__(self, entity: Herbivore, world: World) -> bool:
        target_entitys: list[tuple[Point, Entity]] = world.get_entities(Grass)
        entity_point = world.get_entity_position(entity)
        closest_entity = find_near_entity(entity_point, target_entitys)
        if closest_entity is None:
            return False

        world.remove_entity(closest_entity)
        return True


def find_closest_entity(
    current_point: Point, entities_position: list[tuple[Point, Entity]]
) -> Entity | None:
    max_path = float("inf")
    result_entity = None
    for point, entity in entities_position:
        y_distance = abs(point.y - current_point.y)
        x_distance = abs(point.x - current_point.x)
        current_path = y_distance + x_distance
        if max_path > current_path:
            max_path = current_path
            result_entity = entity

    return result_entity


def find_near_entity[
    T: Entity
](current_point: Point, entities_position: list[tuple[Point, T]]) -> T | None:
    for point, entity in entities_position:
        if closest_point(current_point, point):
            return entity

    return None


def closest_point(current: Point, target: Point) -> bool:
    y_distance = abs(current.y - target.y)
    x_distance = abs(current.x - target.x)
    return not (y_distance > 1 or x_distance > 1)


def find_closest_point_entity(
    current_point: Point,
    entitys_position: list[tuple[Point, Entity]],
    max_path: float = float("inf"),
) -> Point | None:
    result_point = None
    for point, _ in entitys_position:
        y_distance = abs(point.y - current_point.y)
        x_distance = abs(point.x - current_point.x)
        current_path = y_distance + x_distance
        if max_path > current_path:
            max_path = current_path
            result_point = point

    return result_point
