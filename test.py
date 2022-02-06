import os
import signal
import pyautogui as pg
from datetime import datetime
import ctypes
import win32con
import win32gui
import win32process
import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMenu, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, pyqtSlot, Qt

from Hearthstone import GetWindowRectFromName, checkIfProcessRunning, \
    delta, check_state, find_color, setWindow, sleep
from parameters import *

# var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

version = 'v0.05'
window_pos = QRect(0, 30, 400, 1000)
buttom_size = (200, 60)
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.started = False
        self.var = {'win': 1, 'loss': 2, 'error': 3, 'timestamp': datetime.now()}
        self.Header = QLabel('Hearthstone Maker ' + version, self)
        self.start = QPushButton('Start Script', self)
        self.start.clicked.connect(self.on_click_start)
        self.start.setCheckable(True)
        self.start.setGeometry(
            int((window_pos.width()-buttom_size[0])/2), 300, 
            buttom_size[0], buttom_size[1])
        self.stop = QPushButton('Stop Script', self)
        self.stop.clicked.connect(self.on_click_stop)
        self.stop.setCheckable(True)
        self.stop.setGeometry(
            int((window_pos.width()-buttom_size[0])/2), 400, 
            buttom_size[0], buttom_size[1])
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Heathstone Maker")
        self.setGeometry(window_pos)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
    
    @pyqtSlot()
    def on_click_start(self):
        if self.started:
            return
        self.started = True
        while self.started:
            self.stats_text = 'win: %i; loss: %i; error: %i; win rate: %.4f' %\
                (self.var['win'], self.var['loss'], self.var['error'], self.var['win']/(self.var['win']+self.var['loss']))
            print('error: %i' % self.var['error'])
            print(self.stats_text)
            sleep(5, QApplication)
        
    @pyqtSlot()
    def on_click_stop(self):
        if not self.started:
            return
        self.started = False

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
