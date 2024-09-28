import time
from copy import copy

from simulation.actions.base import Action
from simulation.presentation.renderer import Renderer
from simulation.presentation.state import State, Status
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
        self._action_history: list[list[Action]] = []

        for init_action in init_actions:
            init_action(self._world)

    def start(self) -> None:
        self._renderer.clear_frame()
        self._renderer.render(self._world, self._turn_number)
        while True:
            match self._state.status:
                case Status.start:
                    self.make_turn()
                case Status.stop:
                    self._renderer.end_game()
                    break
                case Status.pause:
                    self._renderer.pause_game()
                    time.sleep(1)
                case Status.back:
                    self.undo_turn()

    def make_turn(self) -> None:
        time.sleep(1)
        turn_action_history: list[Action] = []
        for turn_action in self._turn_actions:
            turn_action(self._world)

            turn_action_history.append(copy(turn_action))

        self._turn_number += 1
        self._renderer.render(self._world, self._turn_number)

        self._action_history.append(turn_action_history)

    def undo_turn(self) -> None:
        self._renderer.render(self._world, self._turn_number)

        time.sleep(1)

        try:
            turn_action_history = reversed(self._action_history.pop())
        except IndexError:
            return

        for turn_action in turn_action_history:
            turn_action.undo(self._world)

        self._turn_number -= 1
