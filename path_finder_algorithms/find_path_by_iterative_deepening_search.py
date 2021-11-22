from models import Maze, Terrain
import pygame
import settings



def find_path_by_iterative_deepening_search(screen: pygame.display.set_mode, maze: Maze):

    # helper function
    def _iterative_deepening_search(source: Terrain, target: Terrain, limit: int) -> bool:
        # base cases
        if source == target:
            return True
        if limit <= 0:
            return False

        # mark source terrain as expanded
        sx, sy = source.get_position()
        expanded[sy][sx] = True
        expanded_list.append(source)
        maze.update_terrain_color(screen=screen, terrain=source, color=settings.SEAFOAM)

        # update frontier and terrain.previous_terrain
        for neighbor in source.neighbors:
            ny, nx = neighbor.get_position()
            if neighbor.is_passable() and (not expanded[ny][nx]) and (neighbor not in frontier):
                neighbor.previous_terrain = source
                frontier.append(neighbor)
                maze.update_terrain_color(screen=screen, terrain=neighbor, color=settings.EMERALD)

        # search on neighboring terrains
        for neighbor in source.neighbors:
            ny, nx = neighbor.get_position()
            if neighbor.is_passable() and (not expanded[ny][nx]) and neighbor.previous_terrain == source:
                if _iterative_deepening_search(source=neighbor, target=target, limit=limit - 1):
                    return True

        # default return
        return False

    # initialize frontier and expanded nodes
    max_depth = (maze.x_max + 1) * (maze.y_max + 1) - 1
    frontier = [maze.terrains[maze.start]]
    expanded = [[False for _ in range(maze.x_max + 1)] for _ in range(maze.y_max + 1)]
    expanded_list = []

    # perform iterative deepening search
    for depth_limit in range(max_depth):
        if _iterative_deepening_search(source=maze.terrains[maze.start], target=maze.terrains[maze.end], limit=depth_limit):
            break

        # reset frontier and expanded terrains
        maze.update_terrain_color_simultaneously(screen=screen, terrains=frontier + expanded_list, color=settings.WHITE)
        frontier = [maze.terrains[maze.start]]
        expanded = [[False for _ in range(maze.x_max + 1)] for _ in range(maze.y_max + 1)]
        expanded_list = []