import random
from abc import abstractmethod
from typing import Protocol, override

from simulation.entities import Creature, Entity, Herbivore, Predator, Target
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
    def __call__(self, entity: T, world: World) -> bool:
        """A creature's turn.

        The turn determines whether or not the creature completes the turn.
        True - completes, False - continues
        """

    @abstractmethod
    def undo(self, entity: T, world: World) -> None: ...


class Move(Turn[Creature]):
    def __init__(self, find_path_strategy: FindPathStrategy) -> None:
        self._find_path = find_path_strategy

        self._start_point: Point | None = None

    @override
    def __call__(self, entity: Creature, world: World) -> bool:
        current_point = world.get_entity_position(entity)
        self._start_point = current_point

        target_entitys = world.get_entities(entity.target)
        target_point = find_closest_point_entity(
            current_point,
            target_entitys,
            entity.visual_radius,
        )

        if target_point is None:
            target_point = get_random_near_points(current_point, entity.speed, world)

        path = self._find_path(current_point, target_point, world)

        if len(path) <= entity.speed:
            world.add(path[-1], entity)
            return False

        world.add(path[entity.speed], entity)
        return True

    @override
    def undo(self, entity: Creature, world: World) -> None:
        if self._start_point is not None:
            world.add(self._start_point, entity)


class Starve(Turn[Creature]):
    def __init__(self, power: int) -> None:
        self._power = power
        self._starving_creature: tuple[Point, Creature] | None = None

    @override
    def __call__(self, entity: Creature, world: World) -> bool:
        entity.hp -= self._power

        entity_point = world.get_entity_position(entity)
        self._starving_creature = entity_point, entity
        if entity.hp <= 0:
            world.remove(entity)
            return True
        return False

    @override
    def undo(self, entity: Creature, world: World) -> None:
        if self._starving_creature is None:
            return

        starving_creature = self._starving_creature[1]
        starving_creature.hp += self._power
        if starving_creature.hp > 0:
            world.add(*self._starving_creature)


class Attack(Turn[Predator]):
    def __init__(self) -> None:
        self._attacked_creature: tuple[Point, Creature] | None = None

    @override
    def __call__(self, entity: Predator, world: World) -> bool:
        target_entitys = world.get_entities(Herbivore)
        entity_point = world.get_entity_position(entity)

        closest_entity_result = find_near_entity(entity_point, target_entitys)

        if closest_entity_result is None:
            return False

        closest_entity, closest_entity_point = closest_entity_result
        self._attacked_creature = (closest_entity_point, closest_entity)

        if closest_entity.hp <= 0:
            return False

        closest_entity.hp -= entity.power

        return True

    @override
    def undo(self, entity: Predator, world: World) -> None:
        if self._attacked_creature is None:
            return

        closest_entity = self._attacked_creature[1]
        closest_entity.hp += entity.power


class Eat(Turn[Creature]):
    def __init__(self) -> None:
        self._eated_entity: tuple[Point, Entity] | None = None
        self._current_hp: int | None = None

    @override
    def __call__(self, entity: Creature, world: World) -> bool:
        self._eated_entity = None
        self._current_hp = None

        target_entitys: list[tuple[Point, Target]] = world.get_entities(entity.target)
        entity_point = world.get_entity_position(entity)
        closest_entity_result = find_near_entity(entity_point, target_entitys)

        if closest_entity_result is None:
            return False

        closest_entity, closest_entity_point = closest_entity_result

        if not closest_entity.can_eaten():
            return False

        self._eated_entity = (closest_entity_point, closest_entity)
        self._current_hp = entity.hp
        entity.hp = min(entity.max_hp, entity.hp + closest_entity.nutritional_quality)

        world.remove(closest_entity)
        return True

    @override
    def undo(self, entity: Creature, world: World) -> None:
        if self._eated_entity is not None:
            world.add(*self._eated_entity)

        if self._current_hp is not None:
            entity.hp = self._current_hp


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
](
    current_point: Point,
    entities_position: list[tuple[Point, T]],
) -> (
    tuple[T, Point] | None
):
    for point, entity in entities_position:
        if is_closest_point(current_point, point):
            return entity, point

    return None


def is_closest_point(current: Point, target: Point) -> bool:
    y_distance = abs(current.y - target.y)
    x_distance = abs(current.x - target.x)
    return not (y_distance > 1 or x_distance > 1)


def find_closest_point_entity(
    current_point: Point,
    entitys_position: list[tuple[Point, Target]],
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


def get_random_near_points(
    current_point: Point,
    radius: int,
    world: World,
) -> Point:
    near_points = get_closest_points(current_point, radius)
    near_points = [
        point for point in near_points if point in world and not world.is_used(point)
    ]
    return random.choice(near_points)


def get_closest_points(current: Point, radius: int) -> list[Point]:
    closest_points: list[Point] = []

    for i in range(1, radius + 1):
        closest_points.append(Point(current.x - i, current.y))
        closest_points.append(Point(current.x + i, current.y))
        closest_points.append(Point(current.x, current.y + i))
        closest_points.append(Point(current.x, current.y - i))
        closest_points.append(Point(current.x - i, current.y - i))
        closest_points.append(Point(current.x + i, current.y + i))

    return closest_points
