from . import *
from models import Maze
import pygame
import settings


def find_path(maze: Maze, screen: pygame.display.set_mode):
    # algorithm name to function mapping
    algorithm = {
        "A* Search - Euclidian Heuristic": find_path_by_astar_search_euclidian,
        "A* Search - Manhattan Heuristic": find_path_by_astar_search_manhattan,
        "Bellman-Ford Algorithm": find_path_by_bellman_ford_algorithm,
        "Breadth-First Search": find_path_by_breadth_first_search,
        "Depth-First Search": find_path_by_depth_first_search,
        "Dijkstra's Algorithm": find_path_by_dijkstras_algorithm,
        "Greedy Best First Search - Euclidian": find_path_by_greedy_best_first_search_euclidian,
        "Greedy Best First Search - Manhattan": find_path_by_greedy_best_first_search_manhattan,
        "Iterative Deepening Search": find_path_by_iterative_deepening_search,
        "Uniform Cost Search": find_path_by_uniform_cost_search,
    }

    # perform algorithm
    algorithm_function = algorithm[settings.ALGORITHMS[settings.algo_index]]
    algorithm_function(screen=screen, maze=maze)

    # display path
    maze.display_path_by_backtracking(screen=screen)
