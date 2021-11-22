from random import randint
from .terrain import Terrain
import pygame
import settings


class Maze:

    def __init__(self, gap=10):
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.gap = gap
        self.start = (0, 0)
        self.xmax = settings.WIDTH // gap - 1
        self.ymax = settings.HEIGHT // gap - 1
        self.end = (self.xmax, self.ymax)
        self.terrains = [[Terrain(x, y, gap) for x in range(self.end[0] + 1)] for y in range(self.end[1] + 1)]
        self.on_edit = settings.GRAY
        self.enabled = True
        self.queue = []

    def change_terrain(self, pos):
        if self.mouse_is_over(pos):
            ter_i = self.get_index(pos)
            ter_x, ter_y = ter_i
            if self.on_edit == settings.RED:
                if ter_i != self.end and self.terrains[ter_y][ter_x].color == settings.WHITE:
                    self.start = ter_i
            elif self.on_edit == settings.BLUE:
                if ter_i != self.start and self.terrains[ter_y][ter_x].color == settings.WHITE:
                    self.end = ter_i
            elif self.on_edit == settings.BLACK or self.on_edit == settings.WHITE:
                if ter_i != self.start and ter_i != self.end:
                    self.set_terrain_color(ter_i, self.on_edit)

    def reset(self):
        self.enabled = True
        self.start = (0, 0)
        self.end = (self.xmax, self.ymax)
        self.queue = []
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                terrain.color = settings.WHITE
                terrain.steps = 0

    def clear(self):
        self.enabled = True
        self.queue = []
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                if terrain.color != settings.BLACK:
                    terrain.color = settings.WHITE
                    terrain.steps = 0

    def auto_generate(self):
        self.reset()
        self.start = (randint(0, self.xmax), randint(0, self.ymax))
        self.end = self.start
        while self.end == self.start:
            self.end = (randint(0, self.xmax), randint(0, self.ymax))
        for x in range(0, self.xmax + 1):
            for y in range(0, self.ymax + 1):
                subject = (x, y)
                if subject not in [self.start, self.end]:
                    if randint(0, 2) < 1:
                        self.set_terrain_color((x, y), settings.BLACK)

    def get_index(self, pos):
        return pos[0] // self.gap, pos[1] // self.gap

    def find_route(self, screen):
        self.enabled = False
        self.terrains[self.start[1]][self.start[0]].g = 0
        path_found = False
        self.visit_terrain(screen, self.start)
        if self.queue:
            while True:
                self.visit_terrain(screen, self.queue.pop(0))
                if not self.queue:
                    break
                elif self.queue[0] == self.end:
                    path_found = True
                    break
            if path_found:
                self.trace_back(screen)

    def visit_terrain(self, screen, location):
        self.update_terrain(screen, location, settings.SEAFOAM)
        self.check_neighbors(screen, location)

    def check_neighbors(self, screen, visitor):
        x, y = visitor
        step_count = self.terrains[y][x].g + 1

        neighbors = []
        if x > 0:           neighbors.append((x - 1, y))
        if y > 0:           neighbors.append((x, y - 1))
        if x < self.xmax:   neighbors.append((x + 1, y))
        if y < self.ymax:   neighbors.append((x, y + 1))

        # Adding to Queue
        for neighbor in neighbors:
            self.add_terrain_to_queue(neighbor, step_count, visitor)
            if self.get_terrain_color(neighbor) == settings.WHITE:
                self.update_terrain(screen, neighbor, settings.EMERALD)

    def add_terrain_to_queue(self, location, g, visitor):
        x, y = location
        x2, y2 = visitor
        if settings.ALGORITHMS[settings.algo_index] == "Breadth-First Search" and self.get_terrain_color(location) == settings.WHITE:
            self.queue.append(location)
            self.terrains[y][x].set_last_visit(self.terrains[y2][x2])
        elif settings.ALGORITHMS[settings.algo_index] == "Depth-First Search":
            if self.get_terrain_color(location) == settings.WHITE:
                self.queue.insert(0, location)
                self.terrains[y][x].set_last_visit(self.terrains[y2][x2])
            elif self.get_terrain_color(location) == settings.EMERALD:
                self.queue.insert(0, self.queue.pop(self.queue.index(location)))
        elif settings.ALGORITHMS[settings.algo_index] in ["Dijkstra's Algorithm", "A*"]:
            if self.get_terrain_color(location) == settings.WHITE:
                self.terrains[y][x].g = g
                self.terrains[y][x].update_h(self.end)
                self.terrains[y][x].update_f()
                self.update_queue(location)
                self.terrains[y][x].set_last_visit(self.terrains[y2][x2])

    def update_queue(self, location):
        x, y = location
        for i in range(len(self.queue)):
            if self.terrains[y][x].f < self.terrains[self.queue[i][1]][self.queue[i][0]].f:
                self.queue.insert(i, location)
                break
        else:
            self.queue.append(location)

    def get_terrain_color(self, location):
        return self.terrains[location[1]][location[0]].color

    def set_terrain_color(self, location, color):
        self.terrains[location[1]][location[0]].color = color

    def trace_back(self, screen):
        start = self.end
        while True:
            start = self.get_terrain_last_visitor(start)
            if start == self.start:
                break
            self.update_terrain(screen, start, settings.CHARTREUSE)

    def update_terrain(self, screen, location, color):
        x, y = location
        self.set_terrain_color(location, color)
        pygame.draw.rect(screen, self.get_terrain_color(location), (x * self.gap, y * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.RED, (self.start[0] * self.gap, self.start[1] * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.BLUE, (self.end[0] * self.gap, self.end[1] * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, settings.GRAY, (x * self.gap, y * self.gap, self.gap, self.gap), 1)
        pygame.display.update()

    def get_terrain_last_visitor(self, location):
        last_visit_x = self.terrains[location[1]][location[0]].last_visit.x
        last_visit_y = self.terrains[location[1]][location[0]].last_visit.y
        return last_visit_x, last_visit_y

    @staticmethod
    def mouse_is_over(pos):
        if (0 < pos[0] < settings.WIDTH) and (0 < pos[1] < settings.HEIGHT):
            return True
        return False

    def draw(self, screen):
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                pygame.draw.rect(screen, terrain.color,
                                 (terrain.x * self.gap, terrain.y * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, settings.RED, (self.start[0] * self.gap, self.start[1] * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, settings.BLUE, (self.end[0] * self.gap, self.end[1] * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, settings.GRAY, (terrain.x * self.gap, terrain.y * self.gap, self.gap, self.gap), 1)