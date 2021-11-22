from models import Maze
from random import randint
import settings


def generate_maze_by_randomization(maze: Maze):
    # reset map
    maze.reset()

    # randomize start and end points
    maze.start = (randint(0, maze.x_max), randint(0, maze.y_max))
    maze.end = maze.start
    while maze.end == maze.start:
        maze.end = (randint(0, maze.x_max), randint(0, maze.y_max))

    # randomize terrain color property
    for position, terrain in maze.terrains.items():
        if position in [maze.start, maze.end]:
            continue
        terrain.color = settings.BLACK if randint(0, 2) < 1 else settings.WHITE
