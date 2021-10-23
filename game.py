import pygame
from pygame.locals import *
from CONFIGS import *

from src.game_utils import *


pygame.init()
screen = pygame.display.set_mode((32*HORIZONTAL, 32*VERTICAL))
pygame.display.set_caption('Retro Mall!')
map = TileMap()
player_position = [0,0]

while True: # main game 
    # If the user wants to quit, we quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
    # We render our graphics
    map.draw_map(screen, player_position)
    pygame.display.update()
