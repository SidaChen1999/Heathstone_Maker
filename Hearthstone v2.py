import pyautogui as pg
import time
import keyboard
import psutil
import random
import win32api, win32con, win32gui
from datetime import datetime, timedelta, tzinfo, timezone

while keyboard.is_pressed('s') == False:
    time.sleep(0.05)
print("script starts")

win = 0
loss = 0
errors = 0
img_start = 'G:\Gaming Script\start.jpg'
img_loss = 'G:\Gaming Script\loss.jpg'
img_win = 'G:\Gaming Script\win.jpg'
img_confirm = 'G:\Gaming Script\confirm.jpg'
img_end_turn = 'G:\Gaming Script\end_turn.jpg'
img_enemy_turn = 'G:\Gaming Script\enemy_turn.jpg'
img_my_turn = 'G:\Gaming Script\my_turn.jpg'
img_my_turn1 = 'G:\Gaming Script\my_turn1.jpg'
img_traditional_game = 'G:\Gaming Script\\traditional_game.jpg'
img_play = 'G:\Gaming Script\play.jpg'
img_battlenet = 'G:\Gaming Script\\battlenet.jpg'
img_click = 'G:\Gaming Script\click.jpg'
# regions = (left, top, width, height)
cards = (960, 1200, 600, 50)
minions = (700, 700, 1050, 30)
hero = (1090, 970, 460, 30)
green = (213, 255, 139)
yellow = (255, 255, 12)
red = (255, 255, 89)
enemy_hero = (1298, 415)
states = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
last_states = 0
confi = 0.8
timeout = 120 # seconds

def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
def error(a, b):
    return tuple_abs_sum(tuple_sub(a, b))
epsilon = 20

timestamp = datetime.now()
def check_state(simple=False):
    global states, last_states, timestamp
    last_states = states
    cor_enemy_turn = pg.locateOnScreen(img_enemy_turn, grayscale=False, confidence=confi)
    cor_my_turn = pg.locateOnScreen(img_my_turn, grayscale=False, confidence=confi)
    cor_my_turn1 = pg.locateOnScreen(img_my_turn1, grayscale=False, confidence=confi)
    if cor_enemy_turn != None:
        states = 2
    elif cor_my_turn != None:
        states = 1
    elif cor_my_turn1 != None:
        states = 1
    else:
        states = 0
    if simple:
        return states
    if last_states == states:
        if (datetime.now() - timestamp).seconds > timeout:
            error_state()
            timestamp = datetime.now()
    else:
        timestamp = datetime.now()
    return states

def error_state():
    global errors
    errors += 1
    print('error', errors)
    flag = False
    cor_play = pg.locateOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_play != None:
        x, y = pg.center(cor_play)
        pg.click(x=x,y=y, duration=0.5)
        time.sleep(10)
        flag = True
    elif checkIfProcessRunning('hearthstone'):
        killProcess('hearthstone')
        while pg.locateOnScreen(img_play, grayscale=True, confidence=confi) == None:
            time.sleep(0.5)
            if (datetime.now() - timestamp).seconds > timeout:
                break
        if (datetime.now() - timestamp).seconds > timeout:
            cor_battlenet = pg.locateOnScreen(img_battlenet, grayscale=True, confidence=confi)
            if cor_battlenet != None:
                x, y = pg.center(cor_battlenet)
                pg.click(x=x,y=y, duration=0.5)
                time.sleep(1)
            else:
                return
        x, y = pg.center(pg.locateOnScreen(img_play, grayscale=True, confidence=confi))
        pg.click(x=x,y=y, duration=0.5)
        time.sleep(10)
        flag = True
    elif not checkIfProcessRunning('hearthstone'):
        cor_battlenet = pg.locateOnScreen(img_battlenet, grayscale=True, confidence=confi)
        if cor_battlenet != None:
            x, y = pg.center(cor_battlenet)
            pg.click(x=x,y=y, duration=0.5)
            time.sleep(1)
        cor_play = pg.locateOnScreen(img_play, grayscale=True, confidence=confi)
        if cor_play != None:
            x, y = pg.center(cor_play)
            pg.click(x=x,y=y, duration=0.5)
            time.sleep(10)
        flag = True
    if flag:
        # CN
        while pg.locateOnScreen(img_click, grayscale=False, confidence=confi) == None:
            time.sleep(2)
            if (datetime.now() - timestamp).seconds > timeout:
                    return
        pg.click(x=1280, y=1000, clicks=2, interval=1, duration=0.5)
        while pg.locateOnScreen(img_traditional_game, grayscale=True, confidence=confi) == None:
            time.sleep(2)
            if check_state(simple=True) != 0:
                break
            pg.click(x=1280, y=1000)
            if (datetime.now() - timestamp).seconds > timeout:
                    return
        # NA
        # while pg.locateOnScreen(img_traditional_game, grayscale=True, confidence=confi) == None:
            # time.sleep(2)
            # pg.click(x=1280, y=1000)
            # if check_state(simple=True) != 0:
            #     break
            # if (datetime.now() - timestamp).seconds > timeout:
                # return

last_minion = 0
last_card = 0
def my_turn():
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
                    pg.click(x+minions[0]+20, y+minions[1]+20, duration=0.3)
                else:
                    pg.click(x+minions[0]-20, y+minions[1]+20, duration=0.3)
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

def out_game():
    global win, loss, timestamp
    cor_start = pg.locateOnScreen(img_start, grayscale=True, confidence=confi)
    cor_traditional_game = pg.locateOnScreen(img_traditional_game, grayscale=True, confidence=confi)
    cor_end_turn = pg.locateOnScreen(img_end_turn, grayscale=False, confidence=confi)
    cor_play = pg.locateOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_end_turn != None:
        x, y = pg.center(cor_end_turn)
        pg.click(x=x,y=y, duration=0.3)
        time.sleep(5)
    elif cor_start != None:
        x, y = pg.center(cor_start)
        pg.click(x=x,y=y, duration=0.3)
        time.sleep(5)
        while pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi) == None:
            time.sleep(0.5)
            if (datetime.now() - timestamp).seconds > timeout:
                return
        x, y = pg.center(pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi))
        pg.click(x=x,y=y, duration=0.5)
        time.sleep(2)
        
    elif cor_traditional_game != None:
        x, y = pg.center(cor_traditional_game)
        pg.click(x=x,y=y, duration=0.3)
        time.sleep(2)
    elif cor_play != None:
        error_state()
        timestamp = datetime.now()

    elif pg.locateOnScreen(img_loss, grayscale=True, confidence=confi) != None:
        loss += 1
        print('loss: ', loss, '; win: ', win)
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(x=1280, y=1050)
            time.sleep(1)
            if (datetime.now() - timestamp).seconds > timeout:
                    return
        # pg.click(clicks=5, interval=1, duration=0.5)
    elif pg.locateOnScreen(img_win, grayscale=True, confidence=confi) != None:
        win += 1
        print('loss: ', loss, '; win: ', win)
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(x=1280, y=1050)
            time.sleep(1)
            if (datetime.now() - timestamp).seconds > timeout:
                    return

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def killProcess(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

while keyboard.is_pressed('q') == False:
    try:
        state = check_state()
        print('state: ', state)

        # out of game
        if state == 0:
            out_game()

        # my turn
        elif state == 1:
            my_turn()

        # enemy turn
        elif state == 2:
            time.sleep(1)

    except (KeyboardInterrupt, pg.FailSafeException):
        break
    except:
        error_state()
        timestamp = datetime.now()


print('loss: ', loss, '; win: ', win, '； error: ', errors)
print("script ends")
