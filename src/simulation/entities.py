from dataclasses import dataclass
from typing import ClassVar


class Entity: ...


class Grass(Entity): ...


class Rock(Entity): ...


class Tree(Entity): ...


@dataclass(eq=False)
class Creature(Entity):
    hp: int
    speed: int
    visual_radius: int
    target: ClassVar[type[Entity]]


@dataclass(eq=False)
class Herbivore(Creature):
    target = Grass


@dataclass(eq=False)
class Predator(Creature):
    power: int
    target = Herbivore
