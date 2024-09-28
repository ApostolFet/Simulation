from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, override


class Entity: ...


class Target(ABC, Entity):
    nutritional_quality: int

    @abstractmethod
    def can_eaten(self) -> bool: ...


@dataclass(eq=False)
class Grass(Target):
    nutritional_quality: int

    @override
    def can_eaten(self) -> bool:
        return True


class Rock(Entity): ...


class Tree(Entity): ...


@dataclass(eq=False)
class Creature(Entity):
    target: ClassVar[type[Target]]

    hp: int
    speed: int
    visual_radius: int

    def __post_init__(self) -> None:
        self._max_hp = self.hp

    @property
    def max_hp(self) -> int:
        return self._max_hp


@dataclass(eq=False)
class Herbivore(Target, Creature):
    target = Grass

    nutritional_quality: int

    @override
    def can_eaten(self) -> bool:
        return self.hp <= 0


@dataclass(eq=False)
class Predator(Creature):
    target = Herbivore

    power: int
