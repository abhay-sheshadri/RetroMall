import numpy as np
import pygame
from CONFIGS import *

class TileMap:

    def __init__(self):

        grass = pygame.image.load("assets/grass.png")
        wood = pygame.image.load("assets/wood.png")
        brick = pygame.image.load("assets/bricks.png")
        dirt = pygame.image.load("assets/dirt.png")

        with open("assets/map.txt", "r") as f:
            lines = f.readlines()
            self.base_tiles = np.zeros((len(lines[0]), len(lines)), dtype=object)

            for i in range(len(lines[0])):
                for j in range(len(lines) - 1):
                    
                    if lines[j][i] == "G":
                        self.base_tiles[i, j] = grass
                    elif lines[j][i] == "W":
                        self.base_tiles[i, j] = wood
                    elif lines[j][i] == "B":
                        self.base_tiles[i, j] = brick
                    elif lines[j][i] == "D":
                        self.base_tiles[i, j] = dirt


    def draw_map(self, screen, player_position):
        for i in range(HORIZONTAL):
            for j in range(VERTICAL):
                screen.blit(self.base_tiles[i+player_position[0], j+player_position[1]], (i*32, j*32))



