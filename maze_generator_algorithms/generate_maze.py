from . import generate_maze_by_randomization
from models import Maze
import pygame
import settings


def generate_maze(maze: Maze, screen: pygame.display.set_mode):
    # disable maze to disallow user inputs
    maze.enabled = False

    # algorithm name to function mapping
    algorithm = {
        "Random": generate_maze_by_randomization,
    }

    # perform algorithm
    algorithm_function = algorithm["Random"]
    algorithm_function(maze=maze)

    # enable maze to allow user input
    maze.enabled = True
