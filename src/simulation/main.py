from simulation import Simulation
from simulation.actions import (
    Action,
    SpawnGrassAction,
    SpawnHerbivoreAction,
    SpawnPredatorAction,
    SpawnRockAction,
    SpawnTreeAction,
    TurnAction,
    TurnMap,
)
from simulation.entities import Entity, Grass, Herbivore, Predator, Rock, Tree
from simulation.find_path import BfsFindPathStrategy
from simulation.renderer import Renderer
from simulation.turns import Attack, Eat, Move


def main() -> None:
    entity_icon: dict[type[Entity], str] = {
        Predator: "🐯",
        Herbivore: "🦓",
        Rock: "🪨",
        Grass: "🌱",
        Tree: "🌳",
    }
    default_icon = "🟫"

    find_path_strategy = BfsFindPathStrategy()

    turn_map = TurnMap()
    turn_map.add(Predator, [Move(find_path_strategy), Attack()])
    turn_map.add(Herbivore, [Move(find_path_strategy), Eat()])
    init_actions: list[Action] = [
        SpawnHerbivoreAction(2),
        SpawnPredatorAction(2),
        SpawnTreeAction(2),
        SpawnGrassAction(2),
        SpawnRockAction(2),
    ]
    turn_actions: list[Action] = [TurnAction(turn_map)]
    renderer = Renderer(entity_icon, default_icon)
    simulation = Simulation(20, 10, init_actions, turn_actions, renderer)

    try:
        simulation.start()
    except KeyboardInterrupt:
        print("\rСимуляция завершена")  # noqa: T201


if __name__ == "__main__":
    main()
