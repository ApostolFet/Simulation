from pathlib import Path
from threading import Thread

from simulation import Simulation
from simulation.actions import (
    Action,
    IntervalAction,
    SpawnAction,
    TurnAction,
    TurnMap,
)
from simulation.config import load_config
from simulation.controler import Controler
from simulation.entities import Entity, Grass, Herbivore, Predator, Rock, Tree
from simulation.factory import (
    GrassFactory,
    HerbivoreFactory,
    PredatorFactory,
    RockFactory,
    TreeFactory,
)
from simulation.find_path import (
    AStarFindPathStrategy,
)
from simulation.renderer import Renderer
from simulation.state import State
from simulation.turns import Attack, Eat, Move, Starve
from simulation.world import World


def main() -> None:
    try:
        config = load_config(Path("config.toml"))
    except FileNotFoundError:
        config = load_config(Path("config.example.toml"))

    entity_icon: dict[type[Entity], str] = {
        Predator: config.icon.predator,
        Herbivore: config.icon.herbivore,
        Rock: config.icon.rock,
        Grass: config.icon.grass,
        Tree: config.icon.tree,
    }
    default_icon = config.icon.default
    renderer = Renderer(entity_icon, default_icon)

    find_path_strategy = AStarFindPathStrategy()
    move = Move(find_path_strategy)

    starve = Starve(config.starve.power)

    turn_map = TurnMap()
    turn_map.add(Predator, [starve, move, Attack()])
    turn_map.add(Herbivore, [starve, move, Eat()])

    grass_factory = GrassFactory()
    herbivore_factory = HerbivoreFactory(config.entity.herbivore)

    interval_config = config.spawn.interval
    interval_spawn_actions = [
        IntervalAction(
            interval_config.grass.interval,
            SpawnAction(
                interval_config.grass.count,
                grass_factory,
            ),
        ),
        IntervalAction(
            interval_config.herbivore.interval,
            SpawnAction(
                interval_config.herbivore.count,
                herbivore_factory,
            ),
        ),
    ]

    turn_actions: list[Action] = [TurnAction(turn_map), *interval_spawn_actions]

    predator_factory = PredatorFactory(config.entity.predator)
    tree_factory = TreeFactory()
    rock_factory = RockFactory()

    init_config = config.spawn.init
    init_actions: list[Action] = [
        SpawnAction(init_config.predator, predator_factory),
        SpawnAction(init_config.tree, tree_factory),
        SpawnAction(init_config.rock, rock_factory),
        SpawnAction(init_config.grass, grass_factory),
        SpawnAction(init_config.herbivore, herbivore_factory),
    ]

    state = State()

    world = World(config.world.width, config.world.hight)
    simulation = Simulation(world, init_actions, turn_actions, renderer, state)

    thread = Thread(target=simulation.start)
    thread.start()

    controler = Controler(state)
    controler.get_user_status_game()
