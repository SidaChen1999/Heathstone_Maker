import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMenu, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, pyqtSlot
import pandas as pd
import numpy as np
from functools import partial
import pyautogui as pg
import time
import keyboard
import psutil
from datetime import datetime, timedelta, tzinfo, timezone
from Hearthstone import check_state, error_state, my_turn, out_game, error

version = ''
buttom_size = (200, 60)
window_pos = QRect(1360, 30, 300, 1000)
font = QFont('Arial', 16)
# parameters
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
green2 = (208, 233, 97)
red = (255, 255, 89)
enemy_hero = (1298, 415)
confi = 0.8
timeout = 120 # seconds
epsilon = 20

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.started = False
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.states  = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
        self.last_states = 0
        self.timestamp = datetime.now()
        self.last_minion = 0
        self.last_card = 0

        self.region = [QPushButton('NA', self), QPushButton('CN', self)]
        
        self.output = QLabel('', self)
        self.output.setFont(font)
        self.start = QPushButton('Start Script', self)
        self.start.clicked.connect(self.on_click_start)
        self.start.setGeometry(
            int((window_pos.width()-buttom_size[0])/2), 300, 
            buttom_size[0], buttom_size[1])
        self.stop = QPushButton('Stop Script', self)
        self.stop.setGeometry(
            int((window_pos.width()-buttom_size[0])/2), 400, 
            buttom_size[0], buttom_size[1])
        self.stop.clicked.connect(self.on_click_stop)
        self.setFont(font)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Heathstone Maker")
        self.setGeometry(window_pos)
        
    @pyqtSlot()
    def on_click_start(self):
        self.started = True
        while self.started:
            try:
                state = check_state(self.states, self.last_states, self.timestamp)
                print('state: ', state)
                # out of game
                if state == 0:
                    out_game(self.stats['win'], self.stats['loss'], self.timestamp)
                # my turn
                elif state == 1:
                    my_turn(self.last_minion, self.last_card)
                # enemy turn
                elif state == 2:
                    time.sleep(1)
            except (KeyboardInterrupt, pg.FailSafeException):
                break
            except:
                self.stats['errors'] = error_state(self.stats['errors'])
                self.timestamp = datetime.now()

            QApplication.processEvents()
        return

    @pyqtSlot()
    def on_click_stop(self):
        self.started = False
        return
    


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
