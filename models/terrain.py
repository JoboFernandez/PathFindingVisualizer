import settings
import sys


class Terrain:

    def __init__(self, position: tuple, cost=0, color=settings.WHITE):
        self.x, self.y = position
        self.cost = cost
        self.neighbors = []
        self.source_distance = sys.maxsize
        self.previous_terrain = None
        self.color = color

    def is_passable(self):
        return False if self.color == settings.BLACK else True

    def get_position(self):
        return self.x, self.y

    def restore_defaults(self):
        self.heuristic_distance = 0
        self.previous_terrain = None
        self.color = settings.WHITE

    def heuristic_distance_by_manhattan(self, destination: tuple):
        x = (destination[0] - self.x) if destination[0] > self.x else -(destination[0] - self.x)
        y = (destination[1] - self.y) if destination[1] > self.y else -(destination[1] - self.y)
        return self.source_distance + x + y

    def heuristic_distance_by_euclidian(self, destination: tuple):
        x = (destination[0] - self.x) if destination[0] > self.x else -(destination[0] - self.x)
        y = (destination[1] - self.y) if destination[1] > self.y else -(destination[1] - self.y)
        return self.source_distance + (x ** 2 + y ** 2) ** 0.5
