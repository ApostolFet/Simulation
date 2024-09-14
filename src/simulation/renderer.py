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

    def render(self, world: World) -> None:
        row = [self._default_icon] * world.width
        world_map = [copy(row) for _ in range(world.hight)]
        for point, entity in world.get_all_entitys():
            icon = self._entity_icons[type(entity)]
            world_map[point.y][point.x] = icon

        render_text = ""
        for row in world_map:
            render_text += "".join(row) + "\n"
        clear()
        print(render_text)


def clear() -> None:
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and MacOS
        os.system("clear")
