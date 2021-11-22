from .terrain import Terrain
import pygame
import settings


class Maze:

    def __init__(self, terrain_size=10):
        # dimensions
        self.gap = terrain_size
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.x_max = settings.WIDTH // terrain_size - 1
        self.y_max = settings.HEIGHT // terrain_size - 1

        # status
        self.on_edit = settings.GRAY
        self.enabled = True

        # elements
        self.start = (0, 0)
        self.end = (self.x_max, self.y_max)
        self.terrains = {(x, y): Terrain(position=(x, y)) for x in range(self.x_max + 1) for y in range(self.y_max + 1)}
        self.set_terrain_neighbors()

    def set_terrain_neighbors(self):
        for position in self.terrains:
            neighbor_positions = []

            if position[0] > 0:
                neighbor_positions.append((position[0] - 1, position[1]))
            if position[1] > 0:
                neighbor_positions.append((position[0], position[1] - 1))
            if position[0] < self.x_max:
                neighbor_positions.append((position[0] + 1, position[1]))
            if position[1] < self.y_max:
                neighbor_positions.append((position[0], position[1] + 1))

            for neighbor_position in neighbor_positions:
                self.terrains[position].neighbors.append(self.terrains[neighbor_position])

    def change_edit_status(self, mouse_down: bool, pos: tuple, button_click: int):
        if not self.enabled or not self.mouse_is_over(pos):
            return

        if not mouse_down:
            self.on_edit = settings.GRAY
            return

        if button_click == 1:
            index = self.get_index(pos)
            if index == self.start:
                self.on_edit = settings.RED
            elif index == self.end:
                self.on_edit = settings.BLUE
            else:
                self.on_edit = settings.BLACK

        elif button_click == 3:
            self.on_edit = settings.WHITE

    def change_terrain(self, pos: tuple):
        if self.mouse_is_over(pos):
            position = self.get_index(pos)

            # starting position will be dragged
            if self.on_edit == settings.RED:
                if position != self.end and self.terrains[position].color == settings.WHITE:
                    self.start = position

            # end point will be dragged
            elif self.on_edit == settings.BLUE:
                if position != self.start and self.terrains[position].color == settings.WHITE:
                    self.end = position

            # create or remove terrain obstacles
            elif self.on_edit in [settings.WHITE, settings.BLACK]:
                if position != self.start and position != self.end:
                    self.terrains[position].color = self.on_edit

    def reset(self):
        self.on_edit = settings.GRAY
        self.start = (0, 0)
        self.end = (self.x_max, self.y_max)
        for position, terrain in self.terrains.items():
            terrain.restore_defaults()

    def clear(self):
        self.on_edit = settings.GRAY
        for position, terrain in self.terrains.items():
            if terrain.is_passable():
                terrain.restore_defaults()

    def mouse_is_over(self, pos: tuple) -> bool:
        if (0 < pos[0] < self.width) and (0 < pos[1] < self.height):
            return True
        return False

    def get_index(self, pos: tuple) -> tuple:
        return pos[0] // self.gap, pos[1] // self.gap

    def update_terrain_color(self, screen: pygame.display.set_mode, terrain: Terrain, color: tuple):
        terrain.color = color
        x, y = terrain.get_position()
        sx, sy = self.start
        ex, ey = self.end

        pygame.draw.rect(screen, color, (x * self.gap, y * self.gap, self.gap, self.gap))
        if terrain.get_position() in [self.start, self.end]:
            pygame.draw.rect(screen, settings.RED, (sx * self.gap, sy * self.gap, self.gap, self.gap))
            pygame.draw.rect(screen, settings.BLUE, (ex * self.gap, ey * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.GRAY, (x * self.gap, y * self.gap, self.gap, self.gap), 1)
        pygame.display.update()

    def update_terrain_color_simultaneously(self, screen: pygame.display.set_mode, terrains: list, color: tuple):
        sx, sy = self.start
        ex, ey = self.end
        for terrain in terrains:
            terrain.color = color
            x, y = terrain.get_position()

            pygame.draw.rect(screen, color, (x * self.gap, y * self.gap, self.gap, self.gap))
            if terrain.get_position() in [self.start, self.end]:
                pygame.draw.rect(screen, settings.RED, (sx * self.gap, sy * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, settings.BLUE, (ex * self.gap, ey * self.gap, self.gap, self.gap))
            pygame.draw.rect(screen, settings.GRAY, (x * self.gap, y * self.gap, self.gap, self.gap), 1)

        pygame.display.update()

    def display_path_by_backtracking(self, screen: pygame.display.set_mode):
        # initialize variables
        backtrack_paths = []
        current_terrain = self.terrains[self.end]

        # return if no path found
        if not current_terrain:
            return

        # backtrack
        while True:
            backtrack_paths.append(current_terrain)
            if current_terrain.get_position() == self.start:
                break
            current_terrain = self.terrains[current_terrain.get_position()].previous_terrain

        # draw path
        for terrain in backtrack_paths[::-1]:
            self.update_terrain_color(screen=screen, terrain=terrain, color=settings.CHARTREUSE)

    def draw(self, screen: pygame.display.set_mode):
        # draw terrain colors
        for position, terrain in self.terrains.items():
            x, y = position
            pygame.draw.rect(screen, terrain.color, (x * self.gap, y * self.gap, self.gap, self.gap))
            pygame.draw.rect(screen, settings.GRAY, (x * self.gap, y * self.gap, self.gap, self.gap), 1)

        # draw start and end points
        sx, sy = self.start
        ex, ey = self.end
        pygame.draw.rect(screen, settings.RED, (sx * self.gap, sy * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.BLUE, (ex * self.gap, ey * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.GRAY, (sx * self.gap, sy * self.gap, self.gap, self.gap), 1)
        pygame.draw.rect(screen, settings.GRAY, (ex * self.gap, ey * self.gap, self.gap, self.gap), 1)