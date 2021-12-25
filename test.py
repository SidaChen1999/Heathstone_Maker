import pyautogui as pg
import time
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

import win32con
import win32gui
import win32process

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

# game_window = (0, 0)
# id = checkIfProcessRunning("lingoes")
# if id is not None:
#     hwnds = get_hwnds_for_pid(id)
#     print(hwnds)
# wins = getWindowSizes()
# if len(hwnds) != 0:
#     for win in wins:
#         if hwnds[0] == win[0]:
#             game_window = win[1]
#             print(win[1])
#             break

import logging
import os
import logging
FORMAT = '%(asctime)s %(message)s'
log_file = 'log/'+datetime.now().strftime("%Y-%m-%d,%H;%M;%S")+'.log'
logging.basicConfig(filename=log_file, format=FORMAT, filemode='w')

# logFormatter = logging.Formatter(FORMAT)
logger = logging.getLogger()

# fileHandler = logging.FileHandler(log_file)
# fileHandler.setFormatter(logFormatter)
# logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(consoleHandler)

print(log_file)
logger.setLevel(logging.DEBUG) 
logger.info("script ends")
time.sleep(10)
logging.shutdown()
new = 'log/'+datetime.now().strftime("%Y-%m-%d,%H;%M;%S")+'.log'
os.rename(log_file, new)
