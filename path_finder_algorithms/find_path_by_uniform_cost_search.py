import pygame
import settings


def find_path_by_uniform_cost_search(screen: pygame.display.set_mode, maze):
    # initialize frontier and expanded nodes
    frontier = [maze.terrains[maze.start]]
    expanded = [[False for _ in range(maze.x_max + 1)] for _ in range(maze.y_max + 1)]

    while frontier:
        current_terrain = frontier.pop(0)

        # stop when end point is detected
        if current_terrain.get_position() == maze.end:
            break

        # update frontier and terrain color
        for neighbor in current_terrain.neighbors:
            nx, ny = neighbor.get_position()
            if neighbor.is_passable() and (not expanded[ny][nx]):
                if neighbor not in frontier:
                    neighbor.source_distance = neighbor.cost + current_terrain.source_distance
                    neighbor.previous_terrain = current_terrain
                    frontier.append(neighbor)
                    maze.update_terrain_color(screen=screen, terrain=neighbor, color=settings.EMERALD)
                else:
                    if neighbor.source_distance > neighbor.cost + current_terrain.source_distance:
                        neighbor.source_distance = neighbor.cost + current_terrain.source_distance
                        neighbor.previous_terrain = current_terrain

        # sort frontier by heuristic distance
        frontier = [terrain for terrain in sorted(frontier, key=lambda _terrain: _terrain.source_distance, reverse=True)]

        # update expanded and terrain color
        cx, cy = current_terrain.get_position()
        expanded[cy][cx] = True
        maze.update_terrain_color(screen=screen, terrain=current_terrain, color=settings.SEAFOAM)
