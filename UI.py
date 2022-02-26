import sys
import traceback
import keyboard
from PyQt5.QtWidgets import QApplication, QLineEdit, QMenu, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, pyqtSlot, Qt
import pyautogui as pg
from datetime import datetime, timedelta, tzinfo, timezone
from Hearthstone import GetWindowRectFromName, check_state, error_state,\
    my_turn, out_game, logger_init, logger_deconstruct, setWindow, sleep, update_stats, event
from parameters import *

version = 'v0.0.6'
buttom_size = (200, 60)
window_pos = QRect(0, 30, 400, 1000)
font = QFont('Arial', 14)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.started = False
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.logger_text = 'Logs:\n'
        self.stats_text = 'Stats:\n'
        self.logger = None
        self.param = param()
        
        self.logger_label = QLabel(self.logger_text, self)
        self.logger_label.setGeometry(0, 500, window_pos.width(), 500)
        self.stats_label = QLabel(self.stats_text, self)
        self.stats_label.setGeometry(0, 900, window_pos.width(), 100)
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
        self.setFont(font)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Heathstone Maker")
        self.setGeometry(window_pos)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
    @pyqtSlot()
    def on_click_start(self):
        if self.started:
            return
        self.start.setChecked(True)
        self.stop.setChecked(False)
        self.started = True
        event.clear()

        self.log_file_name = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
        self.logger = logger_init(self.log_file_name)

        rect = GetWindowRectFromName(hwnd_name)
        if rect is None:
            error_state(self.var, self.logger)
            rect = GetWindowRectFromName(hwnd_name)
        else:
            setWindow(hwnd_name, game_window)
            rect = GetWindowRectFromName(hwnd_name)
        if rect is not None:
            self.logger.info('game window: (%i, %i, %i, %i)'%(rect))

        self.logger.info("script starts")
        state = 0
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.update_stats_UI()

        while self.started and keyboard.is_pressed('q') == False:
            try:
                state = check_state(self.var, state)
                self.logger.info('state: %i' % state)
                self.update_log_UI()
                if state == 0:
                    out_game(self.var, self.param, self.logger, self.started)
                    self.update_log_UI()
                elif state == 1:
                    my_turn(self.param)
                elif state == 2:
                    sleep(1, self.started)
                elif state == 3:
                    error_state(self.var, self.logger, self.started)
                    self.var['timestamp'] = datetime.now()
                QApplication.processEvents()
            except (KeyboardInterrupt, pg.FailSafeException):
                break
            except OSError:
                self.logger.info(traceback.format_exc())
                continue
            except:
                self.logger.info(traceback.format_exc())
                try:
                    error_state(self.var, self.logger, self.started)
                    self.var['timestamp'] = datetime.now()
                except:
                    self.logger.info(traceback.format_exc())
                    self.stop.click()
                    break
        
        self.logger.info("script ends")
        update_stats(self.var, self.logger)
        self.update_log_UI()
        logger_deconstruct(self.logger, self.log_file_name)
        self.logger = None

    @pyqtSlot()
    def on_click_stop(self):
        if not self.started:
            return
        self.started = False
        event.set()
        self.start.setChecked(False)
        self.stop.setChecked(True)
    
    def update_log_UI(self):
        with open(self.log_file_name, 'r', encoding='UTF-8') as log_file:
            lines = log_file.readlines()
            self.logger_text = 'Logs:\n' + ''.join([a[11:] for a in lines[-8:]])
            self.logger_label.setText(self.logger_text)
            if lines[-1][24:].startswith(('loss','win')):
                self.update_stats_UI()

    def update_stats_UI(self):
        if self.var['win'] + self.var['loss'] != 0:
            self.stats_text = 'win: %i; loss: %i; error: %i; win rate: %.4f' % \
                (self.var['win'], self.var['loss'], self.var['error'], self.var['win']/(self.var['win']+self.var['loss']))
            self.stats_label.setText('Stats:\n' + self.stats_text)
        else:
            self.stats_label.setText('Stats:\n')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
