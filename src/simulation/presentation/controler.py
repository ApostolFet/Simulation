from simulation.presentation.console import clear_lines
from simulation.presentation.state import State, Status


class Controler:
    def __init__(self, state: State):
        self._state = state

    def get_user_status_game(self) -> None:
        try:
            self._get_status_game()
        except KeyboardInterrupt:
            self._state.status = Status.quit

    def _get_status_game(self) -> None:
        while True:
            result = input()
            if result == "s":
                self._state.status = Status.simulate
            elif result == "p":
                clear_lines(1)
                self._state.status = Status.pause
            elif result == "q":
                self._state.status = Status.quit
                break
            elif result == "r":
                self._state.status = Status.reverse
