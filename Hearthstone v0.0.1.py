import pyautogui as pg
import time
import keyboard
import psutil
import random
import win32api, win32con, win32gui
import datetime


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
epsilon = 10


win = 0
loss = 0
img_start = 'pics/start.jpg'
img_loss = 'pics/loss.jpg'
img_win = 'pics/win.jpg'
img_confirm = 'pics/confirm.jpg'
img_end_turn = 'pics/end_turn.jpg'
img_traditional_game = 'pics/\traditional_game.jpg'
img_play = 'pics/play.jpg'
img_ability = 'pics/\ability.jpg'
cards = (846, 1062, 1647, 1240)
minions = (747, 679, 1728, 868)
green = (213, 255, 139)
red = (255, 255, 89)
enemy_hero = (1298, 415)
states = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn


while keyboard.is_pressed('s') == False:
    time.sleep(0.05)

print("script starts")

while keyboard.is_pressed('q') == False:
    cor_traditional_game = pg.locateOnScreen(img_traditional_game, grayscale=True, confidence=0.8)
    if cor_traditional_game != None:
        x, y = pg.center(cor_traditional_game)
        pg.leftClick(x=x,y=y, duration=0.5)
        time.sleep(2)
    cor_start = pg.locateOnScreen(img_start, grayscale=True, confidence=0.8)
    if cor_start != None:
        x, y = pg.center(cor_start)
        pg.leftClick(x=x,y=y, duration=0.5)
        time.sleep(5)
    cor_confirm = pg.locateOnScreen(img_confirm, grayscale=True, confidence=0.8)
    if cor_confirm != None:
        x, y = pg.center(cor_confirm)
        print('x, y: ', x, ' ', y)
        pg.leftClick(x=x,y=y, duration=0.5)
        time.sleep(1)

    pic = pg.screenshot(region=cards)
    width, height = pic.size
    flag = 0
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            color = pic.getpixel((x, y))
            if tuple_abs_sum(tuple_sub(color, green)) < epsilon:
            #  if color == green:
                flag = 1
                pg.click(x+cards[0], y+cards[1], duration=0.5)
                pg.click(enemy_hero, duration=0.5)
                break
        if flag == 1:
            break
    
    pic = pg.screenshot(region=minions)
    width, height = pic.size
    flag = 0
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            color = pic.getpixel((x, y))
            # if color == green:
            if tuple_abs_sum(tuple_sub(color, green)) < epsilon:
                flag = 1
                pg.click(x+minions[0], y+minions[1], duration=0.5)
                pg.click(enemy_hero, duration=0.5)
        if flag == 1:
            break
    
    cor_ability = pg.locateOnScreen(img_ability, grayscale=False, confidence=0.8)
    if cor_ability != None:
        x, y = pg.center(cor_ability)
        pg.leftClick(x=x,y=y, duration=0.5)
        pg.leftClick(x=enemy_hero, duration=0.5)
        time.sleep(0.5)
    
    cor_end_turn = pg.locateOnScreen(img_end_turn, grayscale=False, confidence=0.8)
    if cor_end_turn != None:
        x, y = pg.center(cor_end_turn)
        pg.leftClick(x=x,y=y, duration=0.5)
        time.sleep(5)
    # pg.leftClick(x=1884, y=689, duration=0.5)
    # time.sleep(5)

    if pg.locateOnScreen(img_loss, grayscale=True, confidence=0.8) != None:
        loss += 1
        print('loss: ', loss, '; win: ', win)
        pg.click(clicks=4, interval=1, duration=0.5)
    if pg.locateOnScreen(img_win, grayscale=True, confidence=0.8) != None:
        win += 1
        print('loss: ', loss, '; win: ', win)
        pg.click(clicks=4, interval=1, duration=0.5)
    if not checkIfProcessRunning('hearthstone'):
        while pg.locateOnScreen(img_play, grayscale=True, confidence=0.8) == None:
            time.sleep(0.5)
        x, y = pg.center(pg.locateOnScreen(img_play, grayscale=True, confidence=0.8))
        pg.leftClick(x=x,y=y, duration=0.5)
        time.sleep(5)

print("script ends")


