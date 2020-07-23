import pygame
import sys
import os

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH, HEIGHT = 600, 600
EXTENSION = 300
window = pygame.display.set_mode((WIDTH + EXTENSION, HEIGHT))

'''
EXTENSION:

SHORTEST-PATH VISUALIZER
<<Algorithm>>

INSTRUCTIONS
Relocate start (Red) and end (Blue) points by mouse drag
Create obstacles by mouse left-click
Erase obstacles by mouse right-click
Press arrow keys to choose from the algorithms
Press Return / Enter key to start route finding
Press R key to reset the whole map
Press C key to clear route

Coded by: Jobo
'''


RED = (255,0,0)                 # Starting Point
BLUE = (0,0,255)                # Ending Point
WHITE = (255,255,255)           # Passable Terrain
BLACK = (0,0,0)                 # Impassable Terrain
GRAY = (100,100,100)            # Terrain Boundary / Neutral
EMERALD = (0,135,15)            # Terrain on Visit Queue
SEAFOAM = (60,235,150)          # Visited Terrain
CHARTREUSE = (210, 215, 105)    # Shortest Path

Algorithms = ["Dijkstra's Algorithm", "A*"]

class Map():
    def __init__(self, gap=15):
        self.width = WIDTH
        self.height = HEIGHT
        self.gap = gap
        self.start = (0,0)
        self.xmax = WIDTH//gap - 1
        self.ymax = HEIGHT//gap - 1
        self.end = (self.xmax, self.ymax)
        self.terrains = [[Terrain(x, y, gap) for x in range(self.end[0]+1)] for y in range(self.end[1]+1)]
        self.on_edit = GRAY
        self.enabled = True
        self.queue = []

    def change_terrain(self, pos):
        if self.on_edit == RED:
            if self.get_index(pos) != self.end:
                self.start = self.get_index(pos)
        elif self.on_edit == BLUE:
            if self.get_index(pos) != self.start:
                self.end = self.get_index(pos)
        elif self.on_edit == BLACK or self.on_edit == WHITE:
            self.terrains[pos[1]//self.gap][pos[0]//self.gap].color = self.on_edit
        
    def reset(self):
        self.enabled = True
        self.start = (0,0)
        self.end = (self.xmax, self.ymax)
        self.queue = []
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                terrain.color = WHITE
                terrain.steps = 0

    def clear(self):
        self.enabled = True
        self.queue = []
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                if terrain.color != BLACK:
                    terrain.color = WHITE
                    terrain.steps = 0

    def get_index(self, pos):
        return (pos[0]//self.gap, pos[1]//self.gap)

    def find_route(self, screen):
        self.enabled = False
        self.visit_terrain(screen, self.start)
        if self.queue:
            while True:
                x, y = self.queue.pop(0)
                self.visit_terrain(screen, (x,y))
                if self.queue[0] == self.end or not self.queue:
                    break
            self.trace_back(screen)

    def check_neighbors(self, screen, location):
        x, y = location
        step_count = self.terrains[y][x].steps + 1
        if x > 0:
            self.check_terrain(screen, (x - 1, y), step_count)
        if x < self.xmax:
            self.check_terrain(screen, (x + 1, y), step_count)
        if y > 0:
            self.check_terrain(screen, (x, y - 1), step_count)
        if y < self.ymax:
            self.check_terrain(screen, (x, y + 1), step_count)

    def check_terrain(self, screen, location, step_count):
        x, y = location
        if self.terrains[y][x].color == WHITE:
            self.update_terrain(screen, (x,y), EMERALD)
            self.terrains[y][x].steps = step_count
            self.queue.append((x,y))

    def visit_terrain(self, screen, location):
        x, y = location
        self.update_terrain(screen, (x,y), SEAFOAM)
        self.check_neighbors(screen, (x,y))

    def trace_back(self, screen):
        start = self.end
        while True:
            start = self.select_minimum_steps(start)
            if start == self.start:
                break
            self.update_terrain(screen, start, CHARTREUSE)

    def select_minimum_steps(self, location):
        x, y = location
        steps = []
        coords = []
        if x > 0:
            xn, yn = x - 1, y
            self.record_steps((xn, yn), steps, coords)
        if x < self.xmax:
            xn, yn = x + 1, y
            self.record_steps((xn, yn), steps, coords)
        if y > 0:
            xn, yn = x, y - 1
            self.record_steps((xn, yn), steps, coords)
        if y < self.ymax:
            xn, yn = x, y + 1
            self.record_steps((xn, yn), steps, coords)
        x, y = coords[steps.index(min(steps))]
        self.terrains[y][x].color = CHARTREUSE
        return (x,y)

    def record_steps(self, location, steps, coords):
        xn, yn = location
        if self.terrains[yn][xn].color == SEAFOAM:
                steps.append(self.terrains[yn][xn].steps)
                coords.append((xn,yn))

    def update_terrain(self, screen, location, color):
        x, y = location
        self.terrains[y][x].color = color
        # self.draw(screen)
        pygame.draw.rect(screen, self.terrains[y][x].color, (x * self.gap, y * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, RED, (self.start[0] * self.gap, self.start[1] * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, BLUE, (self.end[0] * self.gap, self.end[1] * self.gap, self.gap, self.gap))
        pygame.draw.rect(screen, GRAY, (x * self.gap, y * self.gap, self.gap, self.gap), 1)
        pygame.display.update()
    
    def draw(self, screen):
        for terrain_y in self.terrains:
            for terrain in terrain_y:
                pygame.draw.rect(screen, terrain.color, (terrain.x * self.gap, terrain.y * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, RED, (self.start[0] * self.gap, self.start[1] * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, BLUE, (self.end[0] * self.gap, self.end[1] * self.gap, self.gap, self.gap))
                pygame.draw.rect(screen, GRAY, (terrain.x * self.gap, terrain.y * self.gap, self.gap, self.gap), 1)

class Terrain():
    def __init__(self, x, y, gap, color=WHITE):
        self.x = x
        self.y = y
        self.color = color
        self.steps = 0
        self.traced_back = False

map = Map()

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if map.enabled:
                if event.button == 1:
                    if map.get_index(pos) == map.start: map.on_edit = RED
                    elif map.get_index(pos) == map.end: map.on_edit = BLUE
                    else: map.on_edit = BLACK
                elif event.button == 3:
                    map.on_edit = WHITE
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                map.on_edit = GRAY
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    map.reset()
                if event.key == pygame.K_c:
                    map.clear()
                if event.key == pygame.K_RETURN and map.enabled:
                    map.find_route(window)

    map.change_terrain(pos)

    window.fill((150,150,150))
    map.draw(window)
    pygame.display.update()