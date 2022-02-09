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
from PyQt5.QtCore  import *
from PyQt5.QtGui import *

from Hearthstone import GetWindowRectFromName, checkIfProcessRunning, \
    delta, check_state, find_color, setWindow, sleep
from parameters import *

# var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}

class Worker(QObject):
    sgnFinished = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._mutex = QMutex()
        self._running = True

    @pyqtSlot()
    def stop(self):
        print('switching while loop condition to false')
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()

    def running(self):
        try:
            self._mutex.lock()
            return self._running
        finally:
            self._mutex.unlock()

    @pyqtSlot()
    def work(self):
        while self.running():
            pg.time.sleep(5)
            print(datetime.now())
        self.sgnFinished.emit()

class Client(QObject):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._thread = None
        self._worker = None

    def toggle(self, enable):
        if enable:
            if not self._thread:
                self._thread = QThread()

            self._worker = Worker(None)
            self._worker.moveToThread(self._thread)
            self._worker.sgnFinished.connect(self.on_worker_done)

            self._thread.started.connect(self._worker.work)
            self._thread.start()
        else:
            print('stopping the worker object')
            self._worker.stop()

    @pyqtSlot()
    def on_worker_done(self):
        print('workers job was interrupted manually')
        self._thread.quit()
        self._thread.wait()
        if input('\nquit application [Y/N]? ') != 'n':
            QApplication.quit()

if __name__ == '__main__':

    # prevent some harmless Qt warnings
    pyqtRemoveInputHook()

    app = QCoreApplication(sys.argv)

    client = Client(None)

    def start():
        client.toggle(True)
        input('Press something\n')
        client.toggle(False)

    QTimer.singleShot(10, start)

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
