import pyautogui as pg
import time
import keyboard
import psutil
from datetime import datetime
img_start = 'G:\Gaming Script\start.jpg'
img_loss = 'G:\Gaming Script\loss.jpg'
img_win = 'G:\Gaming Script\win.jpg'
img_confirm = 'G:\Gaming Script\confirm.jpg'
img_end_turn = 'G:\Gaming Script\end_turn.jpg'
img_enemy_turn = 'G:\Gaming Script\enemy_turn.jpg'
img_my_turn = 'G:\Gaming Script\my_turn.jpg'
img_traditional_game = 'G:\Gaming Script\\traditional_game.jpg'
img_play = 'G:\Gaming Script\play.jpg'
img_battlenet = 'G:\Gaming Script\\battlenet.jpg'
img_click = 'G:\Gaming Script\click.jpg'
cards = (960, 1200, 600, 50)
minions = (700, 700, 1050, 30)
hero = (1090, 980, 460, 50)
green = (213, 255, 139)
yellow = (255, 255, 12)
red = (255, 255, 89)
enemy_hero = (1298, 415)
states = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
last_states = 0
confi = 0.7
def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
def error(a, b):
    return tuple_abs_sum(tuple_sub(a, b))
epsilon = 15

pic_cards = []
pic_minions = []
pic_hero = []
# global pic_cards, pic_minions, pic_hero

last_minion = 0
last_card = 0
def my_turn():
    global pic_cards, pic_minions, pic_hero
    global last_minion, last_card
    pic_cards = pg.screenshot(region=cards)
    pic_minions = pg.screenshot(region=minions)
    
    width, height = pic_cards.size
    flag = 0
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            color = pic_cards.getpixel((x, y))
            if error(color, green) < epsilon or error(color, yellow) < epsilon:
                flag = 1
                if last_card != x:
                    pg.click(x+cards[0], y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                    # continue
                else:
                    pg.click(x+cards[0]+10, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                last_card = x
                break
        if flag == 1:
            break

    
    width, height = pic_minions.size
    flag = 0
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            color = pic_minions.getpixel((x, y))
            if error(color, green) < epsilon:
                flag = 1
                if last_minion != x:
                    pg.click(x+minions[0]+20, y+minions[1], duration=0.3)
                else:
                    pg.click(x+minions[0]-20, y+minions[1], duration=0.3)
                last_minion = x
                # overcome wall
                pg.click(enemy_hero, duration=0.3)
                break
        if flag == 1:
            break

    pic_hero = pg.screenshot(region=hero)
    width, height = pic_hero.size
    flag = 0
    for x in range(0, width, 3):
        for y in range(0, height, 3):
            color = pic_hero.getpixel((x, y))
            if error(color, green) < epsilon:
                flag = 1
                pg.click(x+hero[0]+10, y+hero[1], duration=0.3)
                #
                pg.click(enemy_hero, duration=0.3)
                break
        if flag == 1:
            break


# while keyboard.is_pressed('s') == False:
#     time.sleep(0.05)
# print("script starts")
# my_turn()
# pic_cards.save('G:\Gaming Script\cards.jpg')
# pic_minions.save('G:\Gaming Script\minions.jpg')
# pic_hero.save('G:\Gaming Script\hero.jpg')

# pg.press('space', presses=1000, interval=0.5)

var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
var['error'] += 1
print(var)