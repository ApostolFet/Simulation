from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from adaptix import Retort

retort = Retort()


@dataclass
class Config:
    world: WorldConfig
    entity: EntityConfig
    spawn: SpawnConfig
    icon: IconConfig
    starve: StarveConfig


@dataclass
class WorldConfig:
    width: int
    hight: int


@dataclass
class EntityConfig:
    herbivore: HerbivoreConfig
    predator: PredatorConfig
    grass: GrassConfig


@dataclass
class HerbivoreConfig:
    hp = 100
    speed = 3
    visual_radius = 10
    nutritional_quality: int


@dataclass
class GrassConfig:
    nutritional_quality: int


@dataclass
class PredatorConfig:
    hp: int
    speed: int
    visual_radius: int
    power: int


@dataclass
class SpawnConfig:
    init: SpawnInitConfig
    interval: SpawnIntervalConfig


@dataclass
class SpawnInitConfig:
    predator: int
    herbivore: int
    tree: int
    grass: int
    rock: int


@dataclass
class SpawnIntervalConfig:
    herbivore: SpawnInterval
    grass: SpawnInterval
    predator: SpawnInterval


@dataclass
class SpawnInterval:
    interval: int
    count: int


@dataclass
class IconConfig:
    predator: str
    herbivore: str
    tree: str
    grass: str
    rock: str
    default: str


@dataclass
class StarveConfig:
    power: int


def load_config(path: Path) -> Config:
    with path.open(mode="rb") as f:
        data = tomllib.load(f)

    config = retort.load(data, Config)
    return config
