import random
from typing import Protocol, override

from simulation.entities import Creature
from simulation.points import Point, find_closest_point_entity, get_closest_points
from simulation.turns.base import Turn
from simulation.world import World


class FindPathStrategy(Protocol):
    def __call__(
        self,
        current_point: Point,
        target_point: Point,
        world: World,
    ) -> list[Point]: ...


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
