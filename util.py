from datetime import datetime
import logging
from tokenize import String
import pyautogui as pg
from parameters import *
from threading import Event
from PyQt5.QtWidgets import QApplication
import win32con
import win32gui
import os
import signal
import subprocess
import csv

event = Event()

def sleep(time, QT:bool=None):
    if QT is None:
        pg.sleep(time)
    else:
        timer = datetime.now()
        while (datetime.now() - timer).seconds < time:
            if event.is_set():
                return
            QApplication.processEvents()
def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
def delta(a, b):
    return tuple_abs_sum(tuple_sub(a, b))
def find_color(pic, step=1, eps=1, *target_colors) -> tuple:
    width, height = pic.size
    for x in range(0, width, step):
        for y in range(0, height, step):
            color = pic.getpixel((x, y))
            for target_color in target_colors:
                if delta(color, target_color) < eps:
                    return(x, y)
    return (None, None)

def check_state_merc(var, param:param, last_state=0, simple=False):
    screenshotIm = pg.screenshot('test_pics/game.jpg', region=param.game_window)
    cor_play = pg.locate(img_play, screenshotIm, grayscale=True, confidence=confi)
    color = pg.pixel(param.my_turn_point[0], param.my_turn_point[1])
    print("state color: ", color)
    if delta(color, my_turn_color) < epsilon or \
       delta(color, my_turn_color_merc) < epsilon:
        print("My turn")
        next_state = 1
    elif delta(color, end_turn_color) < epsilon or \
         delta(color, end_turn_color_merc) < epsilon:
        print("End turn")
        next_state = 4
    elif cor_play != None:
        print("Error")
        next_state = 3
    else:
        print("Out game")
        next_state = 0
    if simple:
        return next_state
    if last_state == next_state:
        if (datetime.now() - var['timestamp']).seconds > timeout:
            next_state = 3
    else:
        var['timestamp'] = datetime.now()
    return next_state

flag = 0
turn_flag = 0
def check_state(var, last_state=0, simple=False):
    global flag, turn_flag
    screenshotIm = pg.screenshot()
    cor_enemy_turn = pg.locate(img_enemy_turn, screenshotIm, grayscale=False, confidence=confi)
    cor_my_turn = pg.locate(img_my_turn, screenshotIm, grayscale=False, confidence=confi)
    cor_play = pg.locate(img_play, screenshotIm, grayscale=True, confidence=confi)
    cor_end_turn = pg.locate(img_end_turn, screenshotIm, grayscale=True, confidence=confi)
    if cor_my_turn != None:
        next_state = 1
    elif cor_enemy_turn != None:
        next_state = 2
    elif cor_play != None:
        next_state = 3
    elif cor_end_turn != None:
        next_state = 4
    else:
        next_state = 0
    if simple:
        return next_state
    if last_state == next_state:
        if (datetime.now() - var['timestamp']).seconds > timeout:
            next_state = 3
        elif last_state == 1:
            print("seconds: ", (datetime.now() - var['timestamp']).seconds)
            if (datetime.now() - var['timestamp']).seconds > 50:
                next_state == 4
                if flag == 0:
                    flag = 1
                elif flag == 1 and turn_flag == 1:
                    next_state = 5
                    flag = 0
                    turn_flag = 0
    else:
        var['timestamp'] = datetime.now()
        if next_state == 2 and flag == 1 and turn_flag == 0:
            turn_flag = 1
        elif turn_flag == 1 and next_state == 4:
            flag = 0
            turn_flag = 0
    return next_state

def end_turn(param:param, QT:bool=None):
    pg.click(param.my_turn_point[0], param.my_turn_point[1], duration=0.2)
    pg.click(param.enemy_hero, clicks=1, interval=0.2, button='RIGHT', duration=0.2)
    sleep(1, QT)
    return

def error_state(var, param:param, logger: logging.Logger=None, QT:bool=None, merc=False):
    var['error'] += 1
    if logger is None:
        print('error: %i' % var['error'])
    else:
        logger.error('error: %i' % var['error'])
    cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_play != None:
        pg.click(cor_play, duration=0.2)
        sleep(10, QT)
    else:
        proc = checkIfProcessRunning(pid_name, kill=True)
        sleep(1, QT)
        if proc == None:
            cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
            if cor_battlenet != None:
                pg.click(cor_battlenet, duration=0.2)
                sleep(1, QT)
            else:
                return
        else:
            cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
            if cor_play == None:
                cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
                if cor_battlenet != None:
                    pg.click(cor_battlenet, duration=0.2)
                    sleep(1, QT)
                else:
                    return
        cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
        if cor_play != None:
            var['timestamp'] = datetime.now()
            pg.click(cor_play, duration=0.2)
            sleep(10, QT)
    while GetWindowRectFromName(hwnd_name) is None:
        if event.is_set():
            return
        sleep(1, QT)
        if (datetime.now() - var['timestamp']).seconds > timeout:
            break
    while pg.locateCenterOnScreen(img_traditional_game, grayscale=True, confidence=confi) == None:
        if event.is_set():
            return
        sleep(1, QT)
        rect = GetWindowRectFromName(hwnd_name)
        if rect != game_window:
            if setWindow(hwnd_name, game_window):
                rect = GetWindowRectFromName(hwnd_name)
                waiting_pos = ((rect[0]+rect[2])/2, rect[1]+870)
            else:
                waiting_pos = screensize
        else:
            waiting_pos = ((rect[0]+rect[2])/2, rect[1]+870)
        pg.click(waiting_pos)
        if merc:
            if check_state_merc(var, param, simple=True) != 0:
                break
        else:
            if check_state(var, param, simple=True) != 0:
                break
        if (datetime.now() - var['timestamp']).seconds > timeout:
            break

def GetWindowRectFromName(name:str)-> tuple:
    hwnd = win32gui.FindWindow(None, name)
    if hwnd == 0:
        return None
    rect = win32gui.GetWindowRect(hwnd)
    return rect

def setWindow(name, rect) -> bool:
    old_rect = GetWindowRectFromName(name)
    if old_rect == rect:
        return True
    if old_rect == None:
        return False
    hwnd = win32gui.FindWindow(None, name)
    placement = win32gui.GetWindowPlacement(hwnd)
    new_placement = list(placement)
    new_placement[0] = -1
    new_placement[1] = win32con.SW_SHOWNORMAL
    new_placement[4] = rect
    win32gui.SetWindowPlacement(hwnd, new_placement)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
        win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
        win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    new_rect = GetWindowRectFromName(name)
    if new_rect == rect:
        return True
    return False

def checkIfProcessRunning(processName:str, kill=False):
    '''Return the process id if it is running or return None'''
    call = 'TASKLIST', '/FI', 'imagename eq %s' % processName
    # use buildin check_output right away
    output = subprocess.check_output(call).decode('gb18030')
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    if last_line.lower().startswith(processName.lower()):
        temp = last_line.split(' ')
        for i in range(1, len(temp)):
            if temp[i] != '':
                pid = int(temp[i])
                if kill:
                    os.kill(pid, signal.SIGTERM)
                return pid
    else: 
        return None

def logger_init(filename='log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'):
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(filename=filename, format=FORMAT, filemode='w', force=True)
    logger = logging.getLogger('Hearthstone.exe')
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(consoleHandler)
    return logger

def logger_deconstruct(logger, filename=None):
    del logging.Logger.manager.loggerDict['Hearthstone.exe']
    del logger
    logging.shutdown()
    if filename is not None:
        log_file_end = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
        try:
            os.rename(filename, log_file_end)
        except:
            print('rename log file error')
    return
    
def update_stats(var, logger:logging.Logger=None, saving=True):
    rows = [] 
    with open('dist/stats.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    if var['win'] + var['loss'] != 0:
        log('win: %i; loss: %i; error: %i; win rate: %.4f' % \
            (var['win'], var['loss'], var['error'], var['win']/(var['win']+var['loss'])), logger)
        rows.append([str(var[a]) for a in var])
        if saving:
            with open('dist/stats.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(header)
                csvwriter.writerows(rows)
    wins, losses = 0, 0
    for row in rows:
        wins += int(row[0])
        losses += int(row[1])
    if wins + losses != 0:
        log('total wins: %i, losses: %i, win rate: %.4f'%(wins, losses, wins/(wins+losses)), logger)
    
def log(str:String, logger:logging.Logger=None):
    if logger is None:
        print(str)
    else:
        logger.info(str)
