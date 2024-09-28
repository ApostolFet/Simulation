from typing import override

from simulation.exceptions import NotFindPathError
from simulation.points import Point, get_closest_points, is_closest_point
from simulation.turns.move import FindPathStrategy
from simulation.world import World


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
            closest_points = get_closest_points(check_point, radius=1)

            for point in closest_points:
                if point not in world or world.is_used(point):
                    continue

                check_q.append((point, [*path, check_point]))

        raise NotFindPathError(f"Path not find from {current_point} to {target_point}")
