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

# var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

class Worker(QObject):
    sgnFinished = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._mutex = QMutex()
        self._running = False

    @pyqtSlot()
    def stop(self):
        print('switching while loop condition to false')
        self._mutex.lock()
        self._running = False
        event.set()
        self._mutex.unlock()
    
    @pyqtSlot()
    def start(self):
        print('starting...')
        self._mutex.lock()
        self._running = True
        event.clear()
        self._mutex.unlock()

    def running(self):
        try:
            self._mutex.lock()
            return self._running
        finally:
            self._mutex.unlock()

    @pyqtSlot()
    def work(self):
        self.var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
        self.param = param()
        state = 0
        while self.running():
            try:
                state = check_state(self.var, state)
                print('state: %i' % state)
                print(datetime.now())
                if state == 0:
                    out_game(self.var, self.param, QT=self.running())
                elif state == 1:
                    my_turn(self.param)
                elif state == 2:
                    sleep(1, self.running())
                elif state == 3:
                    error_state(self.var, QT=self.running())
                    self.var['timestamp'] = datetime.now()
                QApplication.processEvents()
            except (KeyboardInterrupt, pg.FailSafeException):
                break
            except OSError:
                print(traceback.format_exc())
                continue
            except:
                print(traceback.format_exc())
                try:
                    error_state(self.var, QT=self.running())
                    self.var['timestamp'] = datetime.now()
                except:
                    print(traceback.format_exc())
                    break
        self.sgnFinished.emit()

version = 'v0.0.6'
buttom_size = (200, 60)
window_pos = QRect(0, 30, 400, 1000)
font = QFont('Arial', 14)
class Client(QWidget):
    def __init__(self):
        super().__init__()
        self._thread = None
        self._worker = None
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

    pyqtSlot
    def on_click_start(self):
        if not self._thread:
            self._thread = QThread()

        self._worker = Worker(None)
        self._worker.moveToThread(self._thread)
        self._worker.sgnFinished.connect(self.on_worker_done)

        self._thread.started.connect(self._worker.work)
        self._thread.start()
        self._worker.start()
    
    @pyqtSlot()
    def on_click_stop(self):
        print('stopping the worker object')
        self._worker.stop()

    @pyqtSlot()
    def on_worker_done(self):
        print('workers job was interrupted manually')
        self._thread.quit()
        self._thread.wait()
        # if input('\nquit application [Y/N]? ') != 'n':
        #     QCoreApplication.quit()

if __name__ == '__main__':

    # prevent some harmless Qt warnings
    pyqtRemoveInputHook()

    app = QApplication(sys.argv)

    client = Client()
    client.show()

    sys.exit(app.exec_())

# name = hwnd_name
# rect = game_window
# old_rect = GetWindowRectFromName(name)

# hwnd = win32gui.FindWindow(None, name)
# placement = win32gui.GetWindowPlacement(hwnd)
# print('placement: ', placement)
# new_placement = list(placement)
# new_placement[0] = -1
# new_placement[1] = win32con.SW_SHOWNORMAL
# new_placement[4] = game_window
# win32gui.SetWindowPlacement(hwnd, new_placement)
# win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
# win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
#     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
#     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
#     win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# placement = win32gui.GetWindowPlacement(hwnd)
# print('placement: ', placement)
print('ends')

# pg.press('space', presses=1000, interval=0.5)
