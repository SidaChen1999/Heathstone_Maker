import pyautogui as pg
import time
import psutil
from datetime import datetime
import ctypes
import win32con
import win32gui
import win32process

from Hearthstone import delta
from parameters import *

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

# 1080P: (0, 0, 1936, 1119)
# 1440P: (312, 160, 2248, 1279)

game_window = default_game_window
cards = (game_window[0]+650, game_window[1]+990, 600, 50)
minions = (game_window[0]+380, game_window[1]+540, 1050, 30)
enemy_minions = (game_window[0]+390, game_window[1]+335, 1050, 30)
hero = (game_window[0]+780, game_window[1]+810, 460, 30)
enemy_hero = (game_window[0]+922, game_window[1]+153)
waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)


states = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
last_states = 0

pic_cards = pg.screenshot()
pic_minions = pg.screenshot()
pic_hero = pg.screenshot()
pic_enemy_minions = pg.screenshot()

last_minion = 0
last_card = 0
def my_turn(last_minion, last_card):
    global pic_cards, pic_minions, pic_hero, pic_enemy_minions
    pic_cards = pg.screenshot(region=cards)
    pic_minions = pg.screenshot(region=minions)
    
    width, height = pic_cards.size
    flag = 0
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            color = pic_cards.getpixel((x, y))
            if delta(color, green) < epsilon or delta(color, yellow) < epsilon:
                flag = 1
                if last_card != x:
                    pg.click(x+cards[0]-5, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                else:
                    pg.click(x+cards[0]+10, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                last_card = x
                break
        if flag == 1:
            break

    pic_enemy_minions = pg.screenshot(region=enemy_minions)
    width, height = pic_minions.size
    flag = 0
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            color = pic_minions.getpixel((x, y))
            if delta(color, green) < epsilon or delta(color, green2) < epsilon:
                flag = 1
                if last_minion != x:
                    pg.click(x+minions[0]+20, y+minions[1]+20, duration=0.3)
                else:
                    pg.click(x+minions[0]-20, y+minions[1]+20, duration=0.3)
                last_minion = x
                # overcome wall
                target_color = pg.pixel(enemy_hero[0], enemy_hero[1])
                print(target_color)
                pg.click(enemy_hero, duration=0.3)
                return
        if flag == 1:
            break

    pic_hero = pg.screenshot(region=hero)
    width, height = pic_hero.size
    flag = 0
    for x in range(0, width, 3):
        for y in range(0, height, 3):
            color = pic_hero.getpixel((x, y))
            if delta(color, green) < epsilon:
                flag = 1
                pg.click(x+hero[0]+10, y+hero[1], duration=0.3)
                #
                pg.click(enemy_hero, duration=0.3)
                break
        if flag == 1:
            break
    pg.rightClick(duration=0.1)

time.sleep(3)
my_turn(last_minion, last_card)

pic_cards.save('test_pics/cards.jpg')
pic_minions.save('test_pics/minions.jpg')
pic_hero.save('test_pics/hero.jpg')
pic_enemy_minions.save('test_pics/enemy_minions.jpg')
target_color = pg.pixel(enemy_hero[0], enemy_hero[1])
print(enemy_hero)
print(target_color)
print('ends')

# pg.press('space', presses=1000, interval=0.5)


