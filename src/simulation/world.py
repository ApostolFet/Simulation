from simulation.entities import Entity
from simulation.exceptions import EntityNotFoundError, PointAlreadyUsedError
from simulation.points import Point


class World:
    def __init__(self, widht: int, hight: int):
        self.width = widht
        self.hight = hight

        self._map: dict[Entity, Point] = {}
        self._used_points: set[Point] = set()

    def __contains__(self, point: Point) -> bool:
        if point.x < 0 or point.y < 0:
            return False
        return point.x < self.width and point.y < self.hight

    def add(self, point: Point, entity: Entity) -> None:
        """Adds an entity to the map at the given position.
        If the entity is already on the map moves it to the given position

        Raises PointAlreadyUsedError if point already used in world
        """
        current_point = self._map.get(entity)
        if current_point == point:
            return

        if point in self._used_points:
            raise PointAlreadyUsedError

        self._map[entity] = point
        self._used_points.add(point)

        if current_point is None:
            return

        self._used_points.remove(current_point)

    def get_entity_position(self, entity: Entity) -> Point:
        """Get entity position in the world.

        Raise EntityNotFoundError if the entity is not in the world
        """
        point = self._map.get(entity)
        if point is None:
            raise EntityNotFoundError

        return point

    def get_entities[T: Entity](self, entity_type: type[T]) -> list[tuple[Point, T]]:
        return [
            (point, entity)
            for entity, point in self._map.items()
            if isinstance(entity, entity_type)
        ]

    def remove(self, entity: Entity) -> None:
        current_point = self._map.get(entity)
        del self._map[entity]

        if current_point is None:
            return

        self._used_points.remove(current_point)

    def get_all_entitys(self) -> list[tuple[Point, Entity]]:
        return [(point, entity) for entity, point in self._map.items()]

    def is_used(self, point: Point) -> bool:
        return point in self._used_points
