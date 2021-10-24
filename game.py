import pygame
from pygame.locals import *
import random

from CONFIGS import *
from src.game_utils import *
from src.utils import get_pixeled_face, create_new_coupon, get_coupons_from_chain


screen_size = (32*HORIZONTAL, 32*VERTICAL)
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Retro Mall!')
map = TileMap()
player = Player(get_pixeled_face())

clock = pygame.time.Clock()
bg = pygame.image.load("assets/background.png")
browser = None

enemies = [Enemy(map) for i in range(3)]

display_text = None
timer = 0

display_text_2 = None
timer_2 = 0

while True: # main game 
    time_delta = clock.tick(60)/1000.0
    # If the user wants to quit, we quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if browser != None:
                browser.check_for_clicks(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                # Move up
                player.move_up(map)
            if event.key == pygame.K_s:
                # Move down
                player.move_down(map)
            if event.key == pygame.K_a:
                # Move right
                player.move_right(map)
            if event.key == pygame.K_d:
                #Move left
                player.move_left(map)
            if event.key == pygame.K_q:
                display_text_2 = get_coupons_from_chain()
                timer_2 = 600
            in_shop = player.in_store(map)
            if not in_shop and browser != None:
                browser = None
            elif in_shop and browser == None:
                if in_shop == "2":
                    #Open yamaha shop
                    browser = ShopWindow("yamaha")
                elif in_shop == "3":
                    #Open nike shop
                    browser = ShopWindow("nike")
                elif in_shop == "4":
                    # open samsung shop
                    browser = ShopWindow("samsung")
            
    # We render our graphics
    screen.blit(bg, (0,0))
    player.draw_player(screen)
    for i in range(len(enemies)):
        enemies[i].draw(screen)
        if enemies[i].update(map, player.player_location) == "kill":
            enemies.pop(i)
            enemies.append(Enemy(map))
            if random.random() < 0.05:
                display_text = create_new_coupon()
                timer = 600
            break
    if display_text != None and timer > 0:
        screen.blit(display_text, (10, 10))
        timer -= 1
    if display_text_2 != None and timer_2 > 0:
        screen.blit(display_text_2, (10, 10))
        timer_2 -= 1
    if browser != None:
        browser.draw_window(screen)
    pygame.display.update()
