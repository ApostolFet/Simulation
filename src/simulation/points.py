from dataclasses import dataclass

from simulation.entities import Entity, Target


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


def find_near_entity[T: Entity](
    current_point: Point,
    entities_position: list[tuple[Point, T]],
) -> tuple[T, Point] | None:
    for point, entity in entities_position:
        if is_closest_point(current_point, point):
            return entity, point

    return None


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


def get_distance(current_point: Point, target_point: Point) -> int:
    return max(
        abs(current_point.x - target_point.x),
        abs(current_point.y - target_point.y),
    )


def is_closest_point(current: Point, target: Point) -> bool:
    y_distance = abs(current.y - target.y)
    x_distance = abs(current.x - target.x)
    return not (y_distance > 1 or x_distance > 1)
