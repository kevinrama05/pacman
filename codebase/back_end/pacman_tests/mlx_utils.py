from typing import TypedDict


class ParseDict(TypedDict):
    maze: list[str]
    entry: tuple[int, int]
    exit_: tuple[int, int]


def parse_maze_output() -> ParseDict:
    """
    Reads the OUTPUT_FILE and converts its content in a dictionary

    Args:
        None

    Returns:
        dict[str, Union[str, tuple[int, int]]]: The maze's maze, entry, exit
                                                and path
    """
    maze = [[11, 9, 5, 3, 9, 3, 9, 5, 5, 5, 5, 5, 5, 3, 11], [8, 0, 3, 8, 0, 4, 2, 9, 1, 1, 1, 3, 9, 4, 2], [10, 8, 4, 4, 2, 9, 2, 12, 0, 2, 8, 2, 12, 5, 2], [10, 12, 1, 5, 0, 6, 12, 3, 12, 2, 10, 12, 1, 3, 10], [12, 1, 4, 1, 6, 9, 1, 2, 13, 4, 4, 1, 2, 10, 10], [9, 2, 9, 6, 15, 10, 8, 2, 15, 15, 15, 10, 10, 8, 2], [10, 10, 8, 3, 15, 12, 6, 8, 5, 7, 15, 12, 2, 8, 6], [10, 8, 2, 10, 15, 15, 15, 10, 15, 15, 15, 11, 8, 4, 3], [10, 8, 4, 2, 9, 3, 15, 10, 15, 13, 5, 2, 12, 5, 2], [8, 4, 3, 10, 10, 10, 15, 10, 15, 15, 15, 8, 1, 5, 2], [8, 3, 14, 12, 4, 4, 1, 2, 13, 1, 3, 12, 4, 5, 2], [8, 6, 9, 5, 1, 5, 2, 8, 1, 2, 14, 9, 5, 3, 10], [8, 3, 12, 3, 12, 1, 2, 8, 2, 10, 9, 4, 1, 2, 10], [10, 8, 7, 12, 1, 4, 6, 14, 8, 2, 8, 3, 10, 10, 10], [14, 12, 5, 5, 4, 5, 5, 5, 6, 12, 4, 6, 12, 4, 6]]
    maze_hex = []
    maze_line = ''
    for i in maze:
        for j in i:
            maze_line += f"{j:X}"
        maze_hex.append(maze_line)
        maze_line = ''
    entry = (0, 0)
    exit_ = (-1, -1)
    print(maze_hex)

    return ParseDict(
        maze=maze_hex,
        entry=entry,
        exit_=exit_,
    )


def change_seed(new_seed: int) -> None:
    """
    It changes the seed from the configuration file

    Args:
        new_seed (int): The new seed to add in the configuration file

    Returns:
        None
    """
    with open("config.txt", "r") as f:
        lines = f.readlines()
    with open("config.txt", "w") as f:
        for line in lines:
            if "SEED" in line:
                f.write(f"SEED={new_seed}\n")
            else:
                f.write(line)