from models import Maze
from random import shuffle
import pygame
import settings


def find_path_by_bellman_ford_algorithm(screen: pygame.display.set_mode, maze: Maze):
    # initializing the list of terrains
    terrain_list = [terrain for position, terrain in maze.terrains.items() if terrain.color is not settings.BLACK and terrain.get_position() != maze.start]
    shuffle(terrain_list)
    starting_terrain = maze.terrains[maze.start]
    starting_terrain.source_distance = 0
    terrain_list = [starting_terrain] + terrain_list

    # start of bellman-ford iteration
    terrain_count = (maze.x_max + 1) * (maze.y_max + 1)
    for _ in range(terrain_count - 1):
        # initialize loop variables
        has_changes_in_shortest_distance = False
        visited = {terrain.get_position(): False for terrain in terrain_list}

        # check for every terrain
        for current_terrain in terrain_list:
            for neighbor in current_terrain.neighbors:
                if not neighbor.is_passable():
                    continue

                # update neighbor source distance and previous terrain
                if neighbor.source_distance > current_terrain.source_distance + neighbor.cost:
                    neighbor.source_distance = current_terrain.source_distance + neighbor.cost
                    neighbor.previous_terrain = current_terrain
                    has_changes_in_shortest_distance = True

                # apply neighbor color change for visualization
                if not visited[neighbor.get_position()]:
                    maze.update_terrain_color(screen=screen, terrain=neighbor, color=settings.EMERALD)

            # marking the current_terrain as visited
            visited[current_terrain.get_position()] = True
            maze.update_terrain_color(screen=screen, terrain=current_terrain, color=settings.SEAFOAM)

        # break loop if there are no more changes in source_distance attribute for all terrains
        if not has_changes_in_shortest_distance:
            break
