import os
import signal
import pyautogui as pg
from datetime import datetime
import ctypes
import win32con
import win32gui
import win32process

from Hearthstone import GetWindowRectFromName, checkIfProcessRunning, \
    delta, check_state, find_color, setWindow
from parameters import *

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

cards = (game_window[0]+650, game_window[1]+990, 600, 50)
minions = (game_window[0]+380, game_window[1]+540, 1050, 30)
enemy_minions = (game_window[0]+390, game_window[1]+335, 1050, 30)
hero = (game_window[0]+780, game_window[1]+810, 460, 30)
enemy_hero = (game_window[0]+922, game_window[1]+153)
waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)


# pg.sleep(1)
print(datetime.now())
hwnd = win32gui.FindWindow(None, '炉石传说')
print(hwnd)
print(datetime.now())
# hwnd = win32gui.FindWindow(None, 'Battle.net')
if hwnd != 0:
    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] == win32con.SW_SHOWNORMAL:
        print('normal')
    elif placement[1] == win32con.SW_SHOWMAXIMIZED:
        print('maximized')
    elif placement[1] == win32con.SW_SHOWMINIMIZED:
        print('minimized')
    else:
        print('abnormal')
    print(placement)

x, y, cx, cy = game_window
print(game_window)

# SetWindowPos(hwnd, -1, x, y, cx, cy, SWP_NOMOVE|SWP_NOSIZE)
new_placement = list(placement)
new_placement[0] = -2
new_placement[1] = win32con.SW_SHOWNORMAL
new_placement[4] = game_window
# win32gui.SetWindowPos(hwnd, -1, x, y, cx, cy, win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)
# win32gui.SetWindowPlacement(hwnd, new_placement)
setWindow(hwnd_name, game_window)
# win32gui.MoveWindow(hwnd, x, y, cx, cy, True)
placement = win32gui.GetWindowPlacement(hwnd)
print(placement)

print('ends')

# pg.press('space', presses=1000, interval=0.5)


