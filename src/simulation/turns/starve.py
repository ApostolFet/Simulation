from typing import override

from simulation.entities import Creature
from simulation.points import Point
from simulation.turns.base import Turn
from simulation.world import World


class Starve(Turn[Creature]):
    def __init__(self, power: int) -> None:
        self._power = power
        self._starving_creature: tuple[Point, Creature] | None = None

    @override
    def __call__(self, entity: Creature, world: World) -> bool:
        entity.hp -= self._power

        entity_point = world.get_entity_position(entity)
        self._starving_creature = entity_point, entity
        if entity.hp <= 0:
            world.remove(entity)
            return True
        return False

    @override
    def undo(self, entity: Creature, world: World) -> None:
        if self._starving_creature is None:
            return

        starving_creature = self._starving_creature[1]
        starving_creature.hp += self._power
        if starving_creature.hp > 0:
            world.add(*self._starving_creature)
