from threading import Thread

from simulation import Simulation
from simulation.actions import (
    Action,
    IntervalAction,
    SpawnGrassAction,
    SpawnHerbivoreAction,
    SpawnPredatorAction,
    SpawnRockAction,
    SpawnTreeAction,
    TurnAction,
    TurnMap,
)
from simulation.controler import Controler
from simulation.entities import Entity, Grass, Herbivore, Predator, Rock, Tree
from simulation.find_path import (
    AStarFindPathStrategy,
)
from simulation.renderer import Renderer
from simulation.state import State
from simulation.turns import Attack, Eat, Move
from simulation.world import World


def main() -> None:
    entity_icon: dict[type[Entity], str] = {
        Predator: "🐯",
        Herbivore: "🦓",
        Rock: "🪨",
        Grass: "🌱",
        Tree: "🌳",
    }
    default_icon = "🟫"

    find_path_strategy = AStarFindPathStrategy()

    turn_map = TurnMap()
    turn_map.add(Predator, [Move(find_path_strategy), Attack()])
    turn_map.add(Herbivore, [Move(find_path_strategy), Eat()])
    init_actions: list[Action] = [
        SpawnHerbivoreAction(10),
        SpawnPredatorAction(10),
        SpawnTreeAction(10),
        SpawnGrassAction(10),
        SpawnRockAction(10),
    ]
    interval_spawn_actions = [
        IntervalAction(2, SpawnGrassAction(3)),
        IntervalAction(3, SpawnHerbivoreAction(2)),
    ]

    turn_actions: list[Action] = [TurnAction(turn_map), *interval_spawn_actions]
    renderer = Renderer(entity_icon, default_icon)

    state = State()

    controler = Controler(state)
    world = World(50, 20)
    simulation = Simulation(world, init_actions, turn_actions, renderer, state)

    thread = Thread(target=simulation.start)
    thread.start()

    controler.get_user_status_game()


if __name__ == "__main__":
    main()
