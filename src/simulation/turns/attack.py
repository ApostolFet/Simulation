from typing import override

from simulation.entities import Creature, Herbivore, Predator
from simulation.points import Point, find_near_entity
from simulation.turns.base import Turn
from simulation.world import World


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
