from .text import Text
import pygame
import settings


texts = [
    Text(text="PATH-FINDING VISUALIZER", align="center", fontsize=22, pos=(settings.WIDTH, 10), dim=(settings.EXTENSION, 0), bold=True),
    Text(text=f"<< {settings.ALGORITHMS[settings.algo_index]} >>", align = "center", fontsize=18, pos=(settings.WIDTH, 35), dim=(settings.EXTENSION, 0)),
    Text(text="INSTRUCTIONS", align="center", fontsize=20, pos=(settings.WIDTH, 100), dim=(settings.EXTENSION, 0), bold=True),
    Text(text=">> Relocate start (Red) and end (Blue) points by mouse drag", align="left", fontsize=14, pos=(settings.WIDTH, 130), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Create obstacles by mouse left-click", align="left", fontsize=14, pos=(settings.WIDTH, 170), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Erase obstacles by mouse right-click", align="left", fontsize=14, pos=(settings.WIDTH, 190), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Press arrow keys to choose from the algorithms", align="left", fontsize=14, pos=(settings.WIDTH, 210), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Press Return / Enter key to start route finding", align="left", fontsize=14, pos=(settings.WIDTH, 230), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Press R key to reset the whole map", align="left", fontsize=14, pos=(settings.WIDTH, 250), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Press C key to clear route", align="left", fontsize=14, pos=(settings.WIDTH, 270), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text=">> Press P key to randomly generate map paths / obstacles", align="left", fontsize=14, pos=(settings.WIDTH, 290), dim=(settings.EXTENSION, 0), wrap=True),
    Text(text="Programmed by: Jobo", align="right", fontsize=12, pos=(settings.WIDTH, settings.HEIGHT - 20), dim=(settings.EXTENSION, 0)),
]


class Extension:

    def __init__(self):
        self.top = 0
        self.left = settings.WIDTH
        self.width = settings.EXTENSION
        self.height = settings.HEIGHT
        self.objects = texts

    def mouse_is_over(self, pos: tuple) -> bool:
        if (self.left < pos[0] < self.left + self.width) and (self.top < pos[1] < self.top + self.height):
            return True
        return False

    def change_algorithm(self, forward: bool):
        # navigate through settings.ALGORITHMS list
        if forward:
            settings.algo_index += 1
            if settings.algo_index > len(settings.ALGORITHMS) - 1:
                settings.algo_index = 0
        else:
            settings.algo_index -= 1
            if settings.algo_index < 0:
                settings.algo_index = len(settings.ALGORITHMS) - 1

        # update text display
        self.objects[1].text = f"<< {settings.ALGORITHMS[settings.algo_index]} >>"

    def draw(self, window: pygame.display.set_mode):
        for _object in self.objects:
            _object.draw(window)
        pygame.draw.rect(window, settings.BLACK, (self.left, self.top, self.width, self.height), 2)