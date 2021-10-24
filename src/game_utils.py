import numpy as np
import pygame
from CONFIGS import *
from src.db_utils import *
import webbrowser
import random


class TileMap:

    def __init__(self):
        with open("assets/map.txt", "r") as f:
            lines = f.readlines()
            self.base_tiles = [list(s[:-1]) for s in lines]

    
class Player:

    def __init__(self, player_image, initial_pos=[14,24]):
        self.player_image = player_image
        self.player_location = initial_pos
        
    def draw_player(self, screen):
        screen.blit(self.player_image, (self.player_location[1]*32, self.player_location[0] * 32))

    def move_up(self, map):
        if self.player_location[0] == 0:
            return
        if map.base_tiles[self.player_location[0] -1][self.player_location[1]] == "0":
            return
        self.player_location[0] -= 1
    
    def move_right(self, map):
        if self.player_location[1] == 0:
            return
        if map.base_tiles[self.player_location[0]][self.player_location[1] - 1] == "0":
            return
        self.player_location[1] -= 1

    def move_left(self, map):
        if self.player_location[1] == HORIZONTAL - 1:
            return
        if map.base_tiles[self.player_location[0]][self.player_location[1] + 1] == "0":
            return
        self.player_location[1] += 1

    def move_down(self, map):
        if self.player_location[0] == VERTICAL - 1:
            return
        if map.base_tiles[self.player_location[0] +1][self.player_location[1]] == "0":
            return
        self.player_location[0] += 1
    
    def in_store(self, map):
        if map.base_tiles[self.player_location[0]][self.player_location[1]] in "234":
            return map.base_tiles[self.player_location[0]][self.player_location[1]]
        return False


class ShopWindow:

    def __init__(self, brand_name):
        self.brand_name = brand_name
        # Get data from database
        db = DatabaseHandler("product_list.db")
        self.results = db.find(brand_name)
        db.close()
        #
        self.rectangle_links = []
        #
        self.surface = pygame.Surface((1266, 628-50), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.surface, (50,50,50,220), (0,0, 1266, 628))
        
        self.category1 = pygame.Surface((402, 558), pygame.SRCALPHA, 32)
        self.category2 = pygame.Surface((402, 558), pygame.SRCALPHA, 32)
        self.category3 = pygame.Surface((402, 558), pygame.SRCALPHA, 32)

        categories = list(self.results.keys())
        random.shuffle(categories)
        categories = categories[:3]
        self.edit_category_surface(self.category1, categories[0],1)
        self.edit_category_surface(self.category2, categories[1],2)
        self.edit_category_surface(self.category3, categories[2],3)
        #pygame.draw.rect(self.category1, (255, 255, 255, 255), (0, 0, 402, 558))
        #pygame.draw.rect(self.category2, (255, 255, 255, 255), (0, 0, 402, 558))        
        #pygame.draw.rect(self.category3, (255, 255, 255, 255), (0, 0, 402, 558))

        self.surface.blit(self.category1, (15, 10))
        self.surface.blit(self.category2, (15*2+402, 10,))
        self.surface.blit(self.category3, (15*3+402*2, 10,))
        
    def draw_window(self, screen):
        screen.blit(self.surface, (120,150))

    def edit_category_surface(self, surface, category, num):
        random.shuffle(self.results[category])
        results = self.results[category][:3]
        
        for i in range(len(results)):
            result = results[i]
            rect = (0, 5 + 185 * i + 5 * i, 402, 170)
            x = 15 if num > 1 else 0
            self.rectangle_links.append((
                (10+ 120 + 15*(num-1) + x + 402 * (num-1), 180 + 185 * i + 5 * i, rect[2], rect[3]),
                 result['link']))
            # Drawing stuff
            pygame.draw.rect(surface, (255,255,255, 255), rect)
            image = pygame.surfarray.make_surface(result["image"])
            image = pygame.transform.rotate(image, -90)
            image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height()*4))
            surface.blit(image, (10, 20 + 185 * i + 5 * i,))

    def check_for_clicks(self, mouse_pos):
        for rect, link in self.rectangle_links:
            x1, y1, w, h = rect
            x2, y2 = x1+w, y1+h
            x, y = mouse_pos
            if (x1 < x and x < x2):
                if (y1 < y and y < y2):
                    webbrowser.open(link)
                    break
            continue


class Enemy:

    def __init__(self, map):
        self.player_image = pygame.image.load("assets/boss.png")
        self.counter = 0
        while True:
            x = random.randint(0, HORIZONTAL-1)
            y = random.randint(0, VERTICAL-1)
            if map.base_tiles[y][x] == "1":
                self.player_location = [y, x]
                break

    def update(self, map, human_location):
        if human_location[0] == self.player_location[0] and human_location[1] == self.player_location[1]:
            return "kill"
        self.counter += 1
        if self.counter == 40:
            self.counter = 0
            x = random.randint(1,4)
            if x == 1:
                self.move_up(map)
            elif x==2:
                self.move_down(map)
            elif x==3:
                self.move_right(map)
            elif x==4:
                self.move_left(map)

    def draw(self, screen):
        screen.blit(self.player_image, (self.player_location[1]*32, self.player_location[0] * 32))

    def move_up(self, map):
        if self.player_location[0] == 0:
            return
        if map.base_tiles[self.player_location[0] -1][self.player_location[1]] == "0":
            return
        self.player_location[0] -= 1
    
    def move_right(self, map):
        if self.player_location[1] == 0:
            return
        if map.base_tiles[self.player_location[0]][self.player_location[1] - 1] == "0":
            return
        self.player_location[1] -= 1

    def move_left(self, map):
        if self.player_location[1] == HORIZONTAL - 1:
            return
        if map.base_tiles[self.player_location[0]][self.player_location[1] + 1] == "0":
            return
        self.player_location[1] += 1

    def move_down(self, map):
        if self.player_location[0] == VERTICAL - 1:
            return
        if map.base_tiles[self.player_location[0] +1][self.player_location[1]] == "0":
            return
        self.player_location[0] += 1
    