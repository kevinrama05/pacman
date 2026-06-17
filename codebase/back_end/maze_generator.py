from mazegenerator.mazegenerator import MazeGenerator


def maze_generator() -> list[list[int]]:
    maze = MazeGenerator()
    maze.generate()
    return maze._maze
