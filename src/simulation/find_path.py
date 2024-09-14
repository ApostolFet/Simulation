from copy import copy
from typing import override

from simulation.entities import Creature, Entity
from simulation.exceptions import NotFindPathError
from simulation.turns import FindPathStrategy
from simulation.world import Point, World


class BfsFindPathStrategy(FindPathStrategy):
    @override
    def __call__(self, entity: Creature, world: World) -> list[Point]:
        current_point = world.get_entity_position(entity)
        target_entitys = world.get_entities(entity.target)
        target_point = find_closest_point_entity(current_point, target_entitys)
        if target_point is None:
            return [current_point]

        unreacheble_points = {point for point, _ in world.get_all_entitys()}
        path = self.find_path(current_point, target_point, unreacheble_points)
        return path

    def find_path(
        self,
        current_point: Point,
        target_point: Point,
        unreacheble_points: set[Point],
    ) -> list[Point]:
        return self.bfs(current_point, target_point, unreacheble_points)

    @staticmethod
    def bfs(
        current_point: Point,
        target_point: Point,
        unreacheble_points: set[Point],
    ) -> list[Point]:
        checked_point = copy(unreacheble_points)
        checked_point.remove(current_point)

        check_q: list[tuple[Point, list[Point]]] = [(current_point, [])]

        for check_point, path in check_q:
            if check_point in checked_point:
                continue

            if closest_point(check_point, target_point):
                return [*path, check_point]

            checked_point.add(check_point)
            closest_points = get_closest_points(check_point)

            for point in closest_points:
                check_q.append((point, [*path, check_point]))  # noqa: PERF401

        raise NotFindPathError(
            f"Path not find from {current_point} to {target_point}, "
            f"unreacheble_points: {unreacheble_points}"
        )


def get_closest_points(current: Point) -> list[Point]:
    return [
        Point(current.x - 1, current.y),
        Point(current.x + 1, current.y),
        Point(current.x, current.y + 1),
        Point(current.x, current.y - 1),
        Point(current.x - 1, current.y - 1),
        Point(current.x + 1, current.y + 1),
    ]


def closest_point(current: Point, target: Point) -> bool:
    y_distance = abs(current.y - target.y)
    x_distance = abs(current.x - target.x)
    return not (y_distance > 1 or x_distance > 1)


def find_closest_point_entity(
    current_point: Point, entitys_position: list[tuple[Point, Entity]]
) -> Point | None:
    max_path = float("inf")
    result_point = None
    for point, _ in entitys_position:
        y_distance = abs(point.y - current_point.y)
        x_distance = abs(point.x - current_point.x)
        current_path = y_distance + x_distance
        if max_path > current_path:
            max_path = current_path
            result_point = point

    return result_point
