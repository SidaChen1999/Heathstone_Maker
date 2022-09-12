import sys
import traceback
import keyboard
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QMainWindow, QRadioButton, \
    QHBoxLayout, QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import QRect, pyqtSlot, Qt, QTimer
import pyautogui as pg
from datetime import datetime, timedelta, tzinfo, timezone
from Hearthstone import my_turn, out_game, surrender
from Mercenary import my_turn as my_turn_merc
from Mercenary import out_game as out_game_merc
from util import GetWindowRectFromName, check_state, check_state_merc, end_turn, error_state, \
    logger_deconstruct, logger_init, setWindow, sleep, event, update_stats
from parameters import *

version = 'v0.0.7'
buttom_size = (200, 60)
window_pos = QRect(0, 30, 320, 600)
font = QFont('Arial', 14)

class ScrollLabel(QScrollArea):
 
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        self.setWidgetResizable(True)
        self.content = QWidget(self)
        self.setWidget(self.content)
        lay = QVBoxLayout(self.content)
 
        self.label = QLabel(self.content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        self.content.setMinimumWidth(window_pos.width())
        lay.addWidget(self.label)
 
    def setText(self, text):
        self.label.setText(text)
        x = self.verticalScrollBar().maximum()
        self.verticalScrollBar().setValue(x)
        # self.adjustSize()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.started = False
        self.mode = 0
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.logger_text = ""
        self.stats_text = ""
        self.logger = None
        self.param = param()

        self.initUI()
        
    def initUI(self):
        parentLayout = QVBoxLayout()

        self.label = QLabel('Mode: ')
        self.mode1 = QRadioButton('Traditional')
        self.mode1.animateClick()
        self.mode2 = QRadioButton('Mercenary')
        self.mode3 = QRadioButton('Packages')
        self.mode1.toggled.connect(self.onRadioClicked)
        self.mode2.toggled.connect(self.onRadioClicked)
        self.mode3.toggled.connect(self.onRadioClicked)
        modeLayout = QVBoxLayout()
        modeLayout.addWidget(self.label)
        modeLayout.addWidget(self.mode1)
        modeLayout.addWidget(self.mode2)
        modeLayout.addWidget(self.mode3)
        parentLayout.addLayout(modeLayout)

        self.start = QPushButton('Start')
        self.start.clicked.connect(self.on_click_start)
        self.start.setCheckable(True)
        self.start.resize(buttom_size[0], buttom_size[1])
        self.start.setMinimumSize(buttom_size[0], buttom_size[1])
        parentLayout.addWidget(self.start)
        self.stop = QPushButton('Stop')
        self.stop.clicked.connect(self.on_click_stop)
        self.stop.setCheckable(True)
        self.stop.resize(buttom_size[0], buttom_size[1])
        self.stop.setMinimumSize(buttom_size[0], buttom_size[1])
        parentLayout.addWidget(self.stop)

        parentLayout.addWidget(QLabel("Logs:"))
        loggerWidget = QWidget()
        loggerWidget.setMinimumSize(window_pos.width(), 220)
        self.logger_label = ScrollLabel(loggerWidget)
        self.logger_label.setMinimumSize(window_pos.width(), 220)
        self.logger_label.setText(self.logger_text)
        parentLayout.addWidget(loggerWidget)

        parentLayout.addWidget(QLabel("Stats:"))
        statsWidget = QWidget()
        statsWidget.setMinimumSize(window_pos.width(), 80)
        self.stats_label = ScrollLabel(statsWidget)
        self.stats_label.setMinimumSize(window_pos.width(), 80)
        self.stats_label.setText(self.stats_text)
        parentLayout.addWidget(statsWidget)
        
        parentWidget = QWidget()
        parentWidget.setLayout(parentLayout)
        self.setCentralWidget(parentWidget)

        self.setFont(font)
        self.setWindowTitle('Hearthstone Maker ' + version)
        self.move(0, 0)
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
        success = True
        if rect is None:
            error_state(self.var, self.param, self.logger, self.started)
            rect = GetWindowRectFromName(hwnd_name)
        else:
            success = setWindow(hwnd_name, game_window)
            sleep(2, self.started)
            rect = GetWindowRectFromName(hwnd_name)
        if rect is not None:
            self.logger.info('game window: (%i, %i, %i, %i)'%(rect))
        if not success:
            self.param.update(rect)

        self.logger.info("script starts")
        state = 0
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.update_stats_UI()

        while self.started and keyboard.is_pressed('q') == False:
            try:
                if self.mode == 0:
                    state = check_state(self.var, state)
                elif self.mode == 1:
                    state = check_state_merc(self.var, self.param ,state)
                elif self.mode == 2:
                    cnt = 0
                    while self.started and keyboard.is_pressed('space') == False:
                        pg.press('space')
                        sleep(0.2)
                        cnt += 1
                        self.logger.info('Click:  %i' % cnt)
                        self.update_log_UI()
                        QApplication.processEvents()
                    self.logger.info("script ends")
                    logger_deconstruct(self.logger, self.log_file_name)
                    self.logger = None
                    self.stop.animateClick()
                    return
                self.logger.info('state:  %i' % state)
                self.update_log_UI()
                if state == 0:
                    if self.mode == 0:
                        out_game(self.var, self.param, self.logger, self.started)
                    elif self.mode == 1:
                        out_game_merc(self.var, self.param, self.logger, self.started)
                    self.update_log_UI()
                elif state == 1:
                    if self.mode == 0:
                        my_turn(self.param)
                    elif self.mode == 1:
                        my_turn_merc(self.param)
                elif state == 2:
                    sleep(1, self.started)
                elif state == 3:
                    error_state(self.var, self.param, self.logger, self.started)
                    self.var['timestamp'] = datetime.now()
                elif state == 4:
                    end_turn(self.param)
                elif state == 5:
                    surrender(self.logger)
                QApplication.processEvents()
            except (KeyboardInterrupt, pg.FailSafeException):
                self.stop.click()
                break
            except OSError:
                self.logger.info(traceback.format_exc())
                continue
            except:
                self.logger.info(traceback.format_exc())
                try:
                    error_state(self.var, self.param, self.logger, self.started)
                    self.var['timestamp'] = datetime.now()
                except:
                    self.logger.info(traceback.format_exc())
                    self.stop.click()
                    break
        
        self.logger.info("script ends")
        if self.mode == 0:
            update_stats(self.var, self.logger)
        self.update_log_UI()
        logger_deconstruct(self.logger, self.log_file_name)
        self.logger = None
        self.stop.animateClick()

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
            self.logger_text = ''.join([a[11:] for a in lines[-20:]])
            self.logger_label.setText(self.logger_text)
            if lines[-1][24:].startswith(('loss', 'win', 'level', 'round', 'error')):
                self.update_stats_UI()

    def update_stats_UI(self):
        if self.var['win'] + self.var['loss'] != 0:
            self.stats_text = 'win: %i; loss: %i; error: %i; win rate: %.4f' % \
                (self.var['win'], self.var['loss'], self.var['error'], self.var['win']/(self.var['win']+self.var['loss']))
            self.stats_label.setText(self.stats_text)
        else:
            self.stats_label.setText('')
    
    def onRadioClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            if radioBtn.text() == "Traditional":
                self.mode = 0
                print("Mode Traditional")
            elif radioBtn.text() == "Mercenary":
                self.mode = 1
                print("Mode Mercenary")
            elif radioBtn.text() == "Packages":
                self.mode = 2
                print("Mode Packages")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
