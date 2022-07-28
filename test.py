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

from parameters import *
from util import delta

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}
params = param()

color = (51, 189, 17)
if delta(color, end_turn_color) < epsilon:
    print("My turn")
print(delta(color, end_turn_color))

# pg.press('space', presses=1000, interval=0.5)
print('ends')