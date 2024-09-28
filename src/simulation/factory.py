from typing import override

from simulation.actions import EntityFactory
from simulation.config import GrassConfig, HerbivoreConfig, PredatorConfig
from simulation.entities import Grass, Herbivore, Predator, Rock, Tree


class HerbivoreFactory(EntityFactory):
    def __init__(
        self,
        herbivore_config: HerbivoreConfig,
    ) -> None:
        self._hp = herbivore_config.hp
        self._speed = herbivore_config.speed
        self._visual_radius = herbivore_config.visual_radius
        self._nutritional_quality = herbivore_config.nutritional_quality

    @override
    def spawn_entity(self) -> Herbivore:
        return Herbivore(
            hp=self._hp,
            speed=self._speed,
            visual_radius=self._visual_radius,
            nutritional_quality=self._nutritional_quality,
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
    def __init__(
        self,
        grass_config: GrassConfig,
    ) -> None:
        self._nutritional_quality = grass_config.nutritional_quality

    @override
    def spawn_entity(self) -> Grass:
        return Grass(self._nutritional_quality)


class RockFactory(EntityFactory):
    @override
    def spawn_entity(self) -> Rock:
        return Rock()
