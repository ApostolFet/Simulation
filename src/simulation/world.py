from dataclasses import dataclass

from simulation.entities import Entity
from simulation.exceptions import EntityNotFoundError


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class World:
    def __init__(self, widht: int, hight: int):
        self.width = widht
        self.hight = hight

        self._map: dict[Entity, Point] = {}

    def add_entity(self, point: Point, entity: Entity) -> None:
        self._map[entity] = point

    def get_entity_position(self, entity: Entity) -> Point:
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

    def remove_entity(self, entity: Entity) -> None:
        del self._map[entity]

    def get_all_entitys(self) -> list[tuple[Point, Entity]]:
        return [(point, entity) for entity, point in self._map.items()]
