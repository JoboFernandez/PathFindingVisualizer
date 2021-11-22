from models import Maze, Extension
from maze_generator_algorithms import generate_maze
from path_finder_algorithms import find_path
import pygame
import settings
import sys
import os


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode((settings.WIDTH + settings.EXTENSION, settings.HEIGHT))
pygame.display.set_caption("Path-Finding Visualizer")

maze = Maze()
extension = Extension()

while True:
    # get mouse pointer location
    pos = pygame.mouse.get_pos()

    # check for events
    for event in pygame.event.get():

        # quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            maze.change_edit_status(mouse_down=True, pos=pos, button_click=event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            maze.change_edit_status(mouse_down=False, pos=pos, button_click=event.button)

        # keyboard input events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                maze.reset()
                maze.enabled = True
            if event.key == pygame.K_c:
                maze.clear()
                maze.enabled = True
            if maze.enabled:
                if event.key == pygame.K_RETURN:
                    maze.enabled = False
                    find_path(maze=maze, screen=window)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    extension.change_algorithm(forward=True)
                if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                    extension.change_algorithm(forward=False)
                if event.key == pygame.K_p:
                    generate_maze(maze=maze, screen=window)

    # update terrain
    maze.change_terrain(pos)

    # update display
    window.fill((150, 150, 150))
    maze.draw(window)
    extension.draw(window)
    pygame.display.update()
