import heapq
from typing import override

from simulation.exceptions import NotFindPathError
from simulation.turns import FindPathStrategy
from simulation.world import Point, World


class BfsFindPathStrategy(FindPathStrategy):
    @override
    def __call__(
        self,
        current_point: Point,
        target_point: Point,
        world: World,
    ) -> list[Point]:
        checked_point: set[Point] = set()

        check_q: list[tuple[Point, list[Point]]] = [(current_point, [])]

        for check_point, path in check_q:
            if check_point in checked_point:
                continue

            if is_closest_point(check_point, target_point):
                return [*path, check_point]

            checked_point.add(check_point)
            closest_points = get_closest_points(check_point)

            for point in closest_points:
                if point not in world or world.is_used(point):
                    continue

                check_q.append((point, [*path, check_point]))

        raise NotFindPathError(f"Path not find from {current_point} to {target_point}")


class AStarFindPathStrategy(FindPathStrategy):
    @override
    def __call__(
        self,
        current_point: Point,
        target_point: Point,
        world: World,
    ) -> list[Point]:
        checked_points: set[Point] = set()
        heap: list[tuple[int, Point, list[Point]]] = [(1, current_point, [])]

        while heap:
            _, check_point, path = heapq.heappop(heap)
            if check_point in checked_points:
                continue

            if is_closest_point(check_point, target_point):
                return [*path, check_point]

            checked_points.add(check_point)
            closest_points = get_closest_points(check_point)

            for point in closest_points:
                if point not in world or world.is_used(point):
                    continue

                point_path = [*path, check_point]
                distance = get_distance(point, target_point)
                heapq.heappush(heap, (len(point_path) + distance, point, point_path))

        raise NotFindPathError(f"Path not find from {current_point} to {target_point}")


def get_distance(current_point: Point, target_point: Point) -> int:
    return max(
        abs(current_point.x - target_point.x),
        abs(current_point.y - target_point.y),
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


def is_closest_point(current: Point, target: Point) -> bool:
    y_distance = abs(current.y - target.y)
    x_distance = abs(current.x - target.x)
    return not (y_distance > 1 or x_distance > 1)
