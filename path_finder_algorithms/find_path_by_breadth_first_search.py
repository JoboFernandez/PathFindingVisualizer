from models import Maze
import pygame
import settings


def find_path_by_breadth_first_search(screen: pygame.display.set_mode, maze: Maze):
    # initialize frontier and expanded nodes
    frontier = [maze.terrains[maze.start]]
    expanded = [[False for _ in range(maze.x_max + 1)] for _ in range(maze.y_max + 1)]

    # check every terrain in frontier
    while frontier:
        current_terrain = frontier.pop(0)

        # stop when end point is detected
        if current_terrain.get_position() == maze.end:
            break

        # update frontier and terrain color
        for neighbor in current_terrain.neighbors:
            nx, ny = neighbor.get_position()
            if neighbor.is_passable() and (neighbor not in frontier) and (not expanded[ny][nx]):
                frontier.append(neighbor)
                neighbor.previous_terrain = current_terrain
                maze.update_terrain_color(screen=screen, terrain=neighbor, color=settings.EMERALD)

        # update expanded and terrain color
        cx, cy = current_terrain.get_position()
        expanded[cy][cx] = True
        maze.update_terrain_color(screen=screen, terrain=current_terrain, color=settings.SEAFOAM)