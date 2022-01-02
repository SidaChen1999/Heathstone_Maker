import pyautogui as pg
import time
import psutil
from datetime import datetime
import ctypes
import win32con
import win32gui
import win32process

from Hearthstone import delta, error_state

import logging
import os
# FORMAT = '%(asctime)s %(message)s'
# log_file = 'log/'+datetime.now().strftime("%Y-%m-%d,%H;%M;%S")+'.log'
# logging.basicConfig(filename=log_file, format=FORMAT, filemode='w')
# logger = logging.getLogger()
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logging.Formatter(FORMAT))
# logger.addHandler(consoleHandler)

# logger.setLevel(logging.DEBUG) 

def isRealWindow(hWnd) -> bool:
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowSizes() -> list:
    '''
    Return a list of tuples (handler, rect) for each real window.
    Rect is a tuple of (left, top, right, button)
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        windows.append((hWnd, rect))
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def get_hwnds_for_pid (pid):
    def callback (hwnd, hwnds):
        if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
            if found_pid == pid:
                hwnds.append (hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def checkIfProcessRunning(processName, kill=False):
    '''Return the process id if it is running or return None'''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                if kill:
                    proc.kill()
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0),  user32.GetSystemMetrics(1)
print(screensize)
game_window = (0, 0, 0, 0)
id = checkIfProcessRunning("hearthstone")
if id is not None:
    hwnds = get_hwnds_for_pid(id)
    print(hwnds)
    wins = getWindowSizes()
    if len(hwnds) != 0:
        for win in wins:
            if hwnds[0] == win[0]:
                game_window = win[1]
                print(game_window)
                break
# 1080P: (0, 0, 1936, 1119)
# 1440P: (312, 160, 2248, 1279)

img_start = 'pics/start.jpg'
img_loss = 'pics/loss.jpg'
img_win = 'pics/win.jpg'
img_confirm = 'pics/confirm.jpg'
img_end_turn = 'pics/end_turn.jpg'
img_enemy_turn = 'pics/enemy_turn.jpg'
img_my_turn = 'pics/my_turn.jpg'
img_traditional_game = 'pics/traditional_game.jpg'
img_play = 'pics/play.jpg'
img_battlenet = 'pics/battlenet.jpg'
img_click = 'pics/click.jpg'

cards = (game_window[0]+650, game_window[1]+990, 600, 50)
minions = (game_window[0]+390, game_window[1]+540, 1050, 30)
hero = (game_window[0]+780, game_window[1]+810, 460, 30)
enemy_hero = ((game_window[0]+game_window[2])/2, game_window[1]+255)
waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)

green = (213, 255, 139)
green2 = (208, 233, 97)
yellow = (255, 255, 12)
red = (255, 255, 89)
enemy_hero = (1298, 415)
states = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
last_states = 0
confi = 0.7
epsilon = 20

pic_cards = []
pic_minions = []
pic_hero = []
# global pic_cards, pic_minions, pic_hero
last_minion = 0
last_card = 0
def my_turn(last_minion, last_card):
    global pic_cards, pic_minions, pic_hero
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
                    pg.click(x+cards[0]+10, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                    # continue
                else:
                    pg.click(x+cards[0]-10, y+cards[1], duration=0.3)
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
            if delta(color, green) < epsilon or delta(color, green2) < epsilon:
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
            if delta(color, green) < epsilon:
                flag = 1
                pg.click(x+hero[0]+10, y+hero[1], duration=0.3)
                #
                pg.click(enemy_hero, duration=0.3)
                break
        if flag == 1:
            break


# logger.info("script starts")

# my_turn(last_minion, last_card)

# logger.info("script ends")
# logging.shutdown()
# new = 'log/'+datetime.now().strftime("%Y-%m-%d,%H;%M;%S")+'.log'
# os.rename(log_file, new)
# pic_cards.save('test_pics/cards.jpg')
# pic_minions.save('test_pics/minions.jpg')
# pic_hero.save('test_pics/hero.jpg')

import csv
rows = []
with open('dist/stats.csv', 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
if var['loss'] != 0:
    rows.append([str(var[a]) for a in var])
    with open('dist/stats.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(rows)
wins, losses = 0, 0
for row in rows:
    wins += int(row[0])
    losses += int(row[1])
print('ends')

# pg.press('space', presses=1000, interval=0.5)


