from copy import copy
from typing import Any, override

from simulation.actions.base import Action
from simulation.entities import Creature
from simulation.exceptions import EntityNotFoundError
from simulation.turns.base import Turn
from simulation.world import World


class TurnMap:
    def __init__(self) -> None:
        self._turns_creature: dict[type[Creature], list[Turn[Any]]] = {}

    def get[T: Creature](self, creature_type: type[T]) -> list[Turn[T]]:
        return self._turns_creature.setdefault(creature_type, [])

    def add[T: Creature](self, creature_type: type[T], turns: list[Turn[T]]) -> None:
        self._turns_creature.setdefault(creature_type, []).extend(turns)


class TurnAction(Action):
    def __init__(self, turn_map: TurnMap):
        self._turn_map = turn_map
        self._executed_turns: list[tuple[Creature, Turn[Creature]]] = []

    @override
    def __call__(self, world: World) -> None:
        self._executed_turns = []

        all_enititys = world.get_entities(Creature)
        for _, entity in all_enititys:
            if self._is_dead(entity, world):
                continue

            turns = self._turn_map.get(type(entity))
            for turn in turns:
                is_turn_end = turn(entity, world)
                self._executed_turns.append((entity, copy(turn)))
                if is_turn_end:
                    break

    @override
    def undo(self, world: World) -> None:
        for entity, turn in reversed(self._executed_turns):
            turn.undo(entity, world)
        self._executed_turns = []

    def _is_dead(self, creature: Creature, world: World) -> bool:
        if creature.hp <= 0:
            return True

        try:
            world.get_entity_position(creature)
        except EntityNotFoundError:
            return True

        return False
