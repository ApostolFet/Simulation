from typing import override

from simulation.entities import Creature, Entity, Target
from simulation.points import Point, find_near_entity
from simulation.turns.base import Turn
from simulation.world import World


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
