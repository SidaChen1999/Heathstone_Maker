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
import keyboard

from Hearthstone import GetWindowRectFromName, checkIfProcessRunning, \
    delta, check_state, error_state, find_color, my_turn, out_game, setWindow, sleep, event
from parameters import *

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

pg.press('space', presses=1000, interval=0.5)
print('ends')