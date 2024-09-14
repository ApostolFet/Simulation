import time
from itertools import count

from simulation.actions import Action
from simulation.renderer import Renderer
from simulation.world import World


class Simulation:
    def __init__(
        self,
        width: int,
        hight: int,
        init_actions: list[Action],
        turn_actions: list[Action],
        renderer: Renderer,
    ):
        self._world = World(width, hight)
        self._turn_actions = turn_actions
        self._renderer = renderer
        for init_action in init_actions:
            init_action(self._world)

    def start(self) -> None:
        for turn in count(1):
            self._renderer.render(self._world, turn)
            time.sleep(1)
            for turn_action in self._turn_actions:
                turn_action(self._world)
