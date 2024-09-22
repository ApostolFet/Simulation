import time

from simulation.actions import Action
from simulation.renderer import Renderer
from simulation.state import State, Status
from simulation.world import World


class Simulation:
    def __init__(
        self,
        world: World,
        init_actions: list[Action],
        turn_actions: list[Action],
        renderer: Renderer,
        state: State,
    ):
        self._world = world
        self._turn_actions = turn_actions
        self._renderer = renderer
        self._state = state
        self._turn_number = 1

        for init_action in init_actions:
            init_action(self._world)

    def start(self) -> None:
        self._renderer.clear_frame()
        while True:
            match self._state.status:
                case Status.start:
                    self.make_turn()
                case Status.stop:
                    self._renderer.stop_game()
                    break
                case Status.pause:
                    self._renderer.pause_game()
                    time.sleep(1)

    def make_turn(self) -> None:
        self._renderer.render(self._world, self._turn_number)
        time.sleep(1)
        for turn_action in self._turn_actions:
            turn_action(self._world)

        self._turn_number += 1
