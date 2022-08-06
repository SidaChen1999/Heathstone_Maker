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
from util import delta, sleep

var = {'win': 20, 'loss': 30, 'error': 10, 'timestamp': datetime.now()}
params = param()  

color = (213, 172, 13)
if delta(color, my_turn_color_merc) < epsilon:
    print("My turn")
print(delta(color, my_turn_color_merc))

class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making widget resizable
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
 
        # creating label
        self.label = QLabel(content)
 
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)
 
        # adding label to the layout
        lay.addWidget(self.label)
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
 
class Window(QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        # setting title
        self.setWindowTitle("Python ")
 
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
 
        # calling method
        self.UiComponents()
 
        # showing all the widgets
        self.show()
 
    # method for widgets
    def UiComponents(self):
        # text to show in label
        text = "There are so many options provided by Python to develop GUI " \
               "application and PyQt5 is one of them. PyQt5 is cross-platform " \
               "GUI toolkit, a set of python bindings for Qt v5. One can develop" \
               " an interactive desktop application with so much ease because " \
               "of the tools and simplicity provided by this library.A GUI application" \
               " consists of Front-end and Back-end. PyQt5 has provided a tool called " \
               "‘QtDesigner’ to design the front-end by drag and drop method so that " \
               "development can become faster and one can give more time on back-end stuff. "
 
        # creating scroll label
        label = ScrollLabel(self)
 
        # setting text to the label
        label.setText(text)
 
        # setting geometry
        label.setGeometry(100, 100, 200, 80)
 

# App = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(App.exec())

print('ends')