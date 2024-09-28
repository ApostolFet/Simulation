import os
import sys


def clear() -> None:
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and MacOS
        os.system("clear")


def clear_lines(n: int) -> None:
    cursor_up = "\x1b[A"
    erase_line = "\x1b[K"

    for _ in range(n):
        sys.stdout.write(cursor_up)
        sys.stdout.write(erase_line)
