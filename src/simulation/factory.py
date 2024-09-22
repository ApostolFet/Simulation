from typing import override

from simulation.actions import EntityFactory
from simulation.config import HerbivoreConfig, PredatorConfig
from simulation.entities import Grass, Herbivore, Predator, Rock, Tree


class HerbivoreFactory(EntityFactory):
    def __init__(
        self,
        herbivore_config: HerbivoreConfig,
    ) -> None:
        self._hp = herbivore_config.hp
        self._speed = herbivore_config.speed
        self._visual_radius = herbivore_config.visual_radius

    @override
    def spawn_entity(self) -> Herbivore:
        return Herbivore(
            hp=self._hp,
            speed=self._speed,
            visual_radius=self._visual_radius,
        )


class PredatorFactory(EntityFactory):
    def __init__(
        self,
        predator_config: PredatorConfig,
    ) -> None:
        self._hp = predator_config.hp
        self._speed = predator_config.speed
        self._visual_radius = predator_config.visual_radius
        self._power = predator_config.power

    @override
    def spawn_entity(self) -> Predator:
        return Predator(
            hp=self._hp,
            speed=self._speed,
            visual_radius=self._visual_radius,
            power=self._power,
        )


class TreeFactory(EntityFactory):
    @override
    def spawn_entity(self) -> Tree:
        return Tree()


class GrassFactory(EntityFactory):
    @override
    def spawn_entity(self) -> Grass:
        return Grass()


class RockFactory(EntityFactory):
    @override
    def spawn_entity(self) -> Rock:
        return Rock()
