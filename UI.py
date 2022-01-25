import sys
import traceback
from PyQt5.QtWidgets import QApplication, QLineEdit, QMenu, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, pyqtSlot, Qt
import pyautogui as pg
from datetime import datetime, timedelta, tzinfo, timezone
from Hearthstone import check_state, checkIfProcessRunning, error_state,\
    get_hwnds_for_pid, getWindowSizes, my_turn, out_game, logger_init, \
    logger_deconstruct, sleep
from parameters import *

version = 'v0.05'
buttom_size = (200, 60)
window_pos = QRect(0, 30, 400, 1000)
font = QFont('Arial', 16)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.started = False
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.state  = 0 # 0 = out of game; 1 = my turn; 2 = enemy turn; 3 = error
        self.last_minion = 0
        self.last_card = 0
        self.logger_text = 'Logs:\n'
        self.stats_text = 'Stats:\n'
        self.logger = None
        
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
        self.log_file_name = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
        self.logger = logger_init(self.log_file_name)
        screensize = pg.size()
        waiting_pos = (screensize[0]/2, screensize[1]*0.75)
        game_window = default_game_window
        id = checkIfProcessRunning("Hearthstone.exe")
        if id is None:
            error_state(self.var, self.logger)
            id = checkIfProcessRunning("Hearthstone.exe")
        if id is not None:
            hwnds = get_hwnds_for_pid(id)
            wins = getWindowSizes()
            if len(hwnds) != 0:
                for win in wins:
                    if hwnds[0] == win[0]:
                        game_window = win[1]
                        break
        self.logger.info('game window: (%i, %i, %i, %i)'%(game_window))
        # regions = (left, top, width, height)
        cards = (game_window[0]+650, game_window[1]+970, 600, 50)
        minions = (game_window[0]+380, game_window[1]+530, 1050, 30)
        enemy_minions = (game_window[0]+390, game_window[1]+335, 1050, 30)
        hero = (game_window[0]+780, game_window[1]+800, 460, 30)
        enemy_hero = (game_window[0]+922, game_window[1]+153)
        waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)
        self.logger.info("script starts")
        state = 0
        self.var['timestamp'] = datetime.now()
        while self.started:
            try:
                state = check_state(self.var, state)
                self.logger.info('state: %i', state)
                # out_game(self.var, QApplication)
                self.update_log_UI()
                QApplication.processEvents()
            except (KeyboardInterrupt, pg.FailSafeException):
                break
            except OSError:
                self.logger.info(traceback.format_exc())
                continue
            except:
                self.logger.info(traceback.format_exc())
                try:
                    error_state(self.var, waiting_pos, self.logger)
                    self.var['timestamp'] = datetime.now()
                except:
                    self.logger.info(traceback.format_exc())
                    self.stop.click()
                    break

    @pyqtSlot()
    def on_click_stop(self):
        if not self.started:
            return
        self.started = False
        self.logger.info("script ends")
        self.update_log_UI()
        self.start.setChecked(False)
        self.stop.setChecked(True)
        logger_deconstruct(self.logger, self.log_file_name)
        self.logger = None
        return
    
    def update_log_UI(self):
        with open(self.log_file_name, 'r', encoding='UTF-8') as log_file:
            lines = log_file.readlines()
            self.logger_text = 'Logs:\n' + ''.join(lines[-5:])
            self.logger_label.setText(self.logger_text)
            if lines[-1][24:].startswith(('loss','win')):
                self.update_stats_UI()

    def update_stats_UI(self):
        self.stats_text = 'win: %i; loss: %i; error: %i; win rate: %.4f',\
            self.var['win'], self.var['loss'], self.var['error'], self.var['win']/(self.var['win']+self.var['loss'])
        self.stats_label.setText(self.stats_label)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
