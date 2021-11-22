from . import *
from models import Maze
import pygame
import settings


def find_path(maze: Maze, screen: pygame.display.set_mode):
    # algorithm name to function mapping
    algorithm = {
        "Breadth-First Search": find_path_by_bfs,
        "Depth-First Search": find_path_by_dfs,
        "Dijkstra's Algorithm": find_path_by_dijkstras_algorithm,
        "Uniform Cost Search": find_path_by_uniform_cost_search,
        "A* Search - Manhattan Heuristic": find_path_by_astar_search_manhattan,
        "A* Search - Euclidian Heuristic": find_path_by_astar_search_euclidian,
        "Iterative Deepening Search": find_path_by_iterative_deepening_search,
    }

    # perform algorithm
    algorithm_function = algorithm[settings.ALGORITHMS[settings.algo_index]]
    algorithm_function(screen=screen, maze=maze)

    # display path
    maze.display_path_by_backtracking(screen=screen)
