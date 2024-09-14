import os
from copy import copy

from simulation.entities import Entity
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

        render_world = ""
        for row in world_map:
            render_world += "".join(row) + "\n"

        render_statistic = "\n"
        for icon, count in count_entitys.items():
            render_statistic += f"{icon}: {count}\n"

        clear()
        print(render_world)
        print(f"Turn: {turn}")
        print(render_statistic)


def clear() -> None:
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and MacOS
        os.system("clear")
