import heapq
from typing import override

from simulation.exceptions import NotFindPathError
from simulation.points import Point, get_closest_points, get_distance, is_closest_point
from simulation.turns.move import FindPathStrategy
from simulation.world import World


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
            closest_points = get_closest_points(check_point, radius=1)

            for point in closest_points:
                if point not in world or world.is_used(point):
                    continue

                point_path = [*path, check_point]
                distance = get_distance(point, target_point)
                heapq.heappush(heap, (len(point_path) + distance, point, point_path))

        raise NotFindPathError(f"Path not find from {current_point} to {target_point}")
