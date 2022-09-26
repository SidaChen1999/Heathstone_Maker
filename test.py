import os
import random
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
from util import delta, sleep

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}
params = param()  

color = (213, 172, 13)
if delta(color, my_turn_color_merc) < epsilon:
    print("My turn")
print(delta(color, my_turn_color_merc))

tup = (1,2,3)
print("something %s" % (tup,))

print('ends')