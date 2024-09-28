from copy import copy

from simulation.entities import Entity
from simulation.presentation.console import clear, clear_lines
from simulation.world import World


class Renderer:
    def __init__(
        self,
        entity_icons: dict[type[Entity], str],
        default_icon: str,
    ):
        self._entity_icons = entity_icons
        self._default_icon = default_icon

    def render(self, world: World, turn: int) -> None:
        row = [self._default_icon] * world.width
        world_map = [copy(row) for _ in range(world.hight)]

        all_entitys = world.get_all_entitys()
        count_entitys: dict[str, int] = {}

        for point, entity in all_entitys:
            icon = self._entity_icons[type(entity)]
            world_map[point.y][point.x] = icon

            current_count = count_entitys.setdefault(icon, 0)
            count_entitys[icon] = current_count + 1

        lines_render = 0
        render_world = ""
        for row in world_map:
            lines_render += 1
            render_world += "".join(row) + "\n"

        render_statistic = "\n"
        for icon, count in count_entitys.items():
            lines_render += 1
            render_statistic += f"{icon}: {count}\n"

        cli_lines = 10

        clear_lines(lines_render + cli_lines)
        print(render_world)
        print(f"Turn: {turn}")
        print(render_statistic)
        print(
            "Enter s - to simulate, p - to pause, "
            "r - to reverse simulate, q - to quit: \r"
        )

    def end_game(self) -> None:
        print("\rSimulation finished")

    def pause_game(self) -> None:
        clear_lines(1)
        print("Enter s - to simulate, r - to reverse simulate, q - to quit: \r")

    def clear_frame(self) -> None:
        clear()
