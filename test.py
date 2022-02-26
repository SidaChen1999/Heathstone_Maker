import os
import signal
import traceback
import pyautogui as pg
from datetime import datetime
import ctypes
import win32con
import win32gui
import win32process
import sys
from PyQt5.QtCore  import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Hearthstone import GetWindowRectFromName, checkIfProcessRunning, \
    delta, check_state, error_state, find_color, my_turn, out_game, setWindow, sleep, event
from parameters import *

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

name = hwnd_name
rect = game_window
old_rect = GetWindowRectFromName(name)

hwnd = win32gui.FindWindow(None, name)
placement = win32gui.GetWindowPlacement(hwnd)
print('placement: ', placement)
new_placement = list(placement)
new_placement[0] = -1
new_placement[1] = win32con.SW_SHOWNORMAL
new_placement[4] = game_window
win32gui.SetWindowPlacement(hwnd, new_placement)
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
    win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
placement = win32gui.GetWindowPlacement(hwnd)
print('placement: ', placement)
print('ends')

# pg.press('space', presses=1000, interval=0.5)
