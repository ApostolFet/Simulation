from dataclasses import dataclass


class Entity: ...


@dataclass(eq=False)
class Creature(Entity):
    hp: int
    speed: int
    target: type[Entity]


@dataclass(eq=False)
class Predator(Creature):
    power: int


@dataclass(eq=False)
class Herbivore(Creature): ...


class Grass(Entity): ...


class Rock(Entity): ...


class Tree(Entity): ...
