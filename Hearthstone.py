#!/usr/bin/env python
from typing import Literal
import pyautogui as pg
import keyboard
from datetime import datetime
import csv
import logging
import traceback
import win32con
import win32gui
import win32process
import os
import signal
import subprocess
from PyQt5.QtWidgets import QApplication
from parameters import *

def sleep(time, QT: QApplication=None):
    if QT is None:
        pg.sleep(time)
    else:
        timer = datetime.now()
        while (datetime.now() - timer).seconds < time:
            QT.processEvents()
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

def check_state(var, last_state, simple=False):
    screenshotIm = pg.screenshot()
    cor_enemy_turn = pg.locate(img_enemy_turn, screenshotIm, grayscale=False, confidence=confi)
    cor_my_turn = pg.locate(img_my_turn, screenshotIm, grayscale=False, confidence=confi)
    cor_my_turn1 = pg.locate(img_my_turn1, screenshotIm, grayscale=False, confidence=confi)
    cor_play = pg.locate(img_play, screenshotIm, grayscale=True, confidence=confi)
    if cor_enemy_turn != None:
        next_state = 2
    elif cor_my_turn != None:
        next_state = 1
    elif cor_my_turn1 != None:
        next_state = 1
    elif cor_play != None:
        next_state = 3
    else:
        next_state = 0
    if simple:
        return next_state
    if last_state == next_state:
        if (datetime.now() - var['timestamp']).seconds > timeout:
            next_state = 3
    else:
        var['timestamp'] = datetime.now()
    return next_state

def error_state(var, logger: logging.Logger=None, QT=None):
    var['error'] += 1
    if logger is not None:
        logger.error('error: %i', var['error'])
    cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_play != None:
        pg.click(cor_play, duration=0.5)
        print(1)
        sleep(10, QT)
    else:
        proc = checkIfProcessRunning('Hearthstone.exe', kill=True)
        print(2)
        sleep(2, QT)
        if proc == None:
            cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
            if cor_battlenet != None:
                pg.click(cor_battlenet, duration=0.5)
                print(3)
                sleep(1, QT)
            else:
                return
        else:
            cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
            if cor_play == None:
                cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
                if cor_battlenet != None:
                    pg.click(cor_battlenet, duration=0.5)
                    print(4)
                    sleep(1, QT)
                else:
                    return
        cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
        if cor_play != None:
            var['timestamp'] = datetime.now()
            pg.click(cor_play, duration=0.5)
            print(5)
            sleep(10, QT)
    while pg.locateCenterOnScreen(img_traditional_game, grayscale=True, confidence=confi) == None:
        print(6)
        sleep(2, QT)
        pg.click(waiting_pos, duration=0.2)
        if check_state(var, state, simple=True) != 0:
            break
        if (datetime.now() - var['timestamp']).seconds > timeout:
            return
    print(7)

def my_turn():
    pic_cards = pg.screenshot('test_pics/cards.jpg', region=cards)
    pic_minions = pg.screenshot('test_pics/minions.jpg', region=minions)
    pic_hero = pg.screenshot('test_pics/hero.jpg', region=hero)
    
    x_cards, y_cards = find_color(pic_cards, 2, epsilon, green, yellow)
    if x_cards is not None:
        pg.click(x_cards+cards[0], y_cards+cards[1]+20, duration=0.2)
        pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.2)

    x_minions, y_minions = find_color(pic_minions, 5, epsilon, green, green2)
    if x_minions is not None:
        pg.click(x_minions+minions[0], y_minions+minions[1]+40, duration=0.2)
        enemy_hero_color = pg.pixel(enemy_hero[0], enemy_hero[1])
        if delta(enemy_hero_color, red) < epsilon+40:
            pg.click(enemy_hero, duration=0.2)
        else:
            pic_enemy_minions = pg.screenshot('test_pics/enemy_minions.jpg', region=enemy_minions)
            x_enemy, y_enemy = find_color(pic_enemy_minions, 5, epsilon, red)
            if x_enemy is not None:
                pg.click(x_enemy+enemy_minions[0]+20, y_enemy+enemy_minions[1]+40, duration=0.2)
            else:
                pg.click(enemy_hero, duration=0.2)

    if x_minions is None and x_cards is None:
        x_hero, y_hero = find_color(pic_hero, 3, epsilon, green)
        if x_hero is not None:
            pg.click(x_hero+hero[0], y_hero+hero[1]+30, duration=0.2)
            pg.click(enemy_hero, duration=0.2)
    pg.click(enemy_hero, clicks=2, interval=0.2, button='RIGHT', duration=0.2)

def out_game(var, QT=None):
    screenshotIm = pg.screenshot()
    cor_start = pg.locate(img_start, screenshotIm, grayscale=True, confidence=confi)
    cor_traditional_game = pg.locate(img_traditional_game, screenshotIm, grayscale=True, confidence=confi)
    cor_end_turn = pg.locate(img_end_turn, screenshotIm, grayscale=False, confidence=confi)
    if cor_end_turn != None:
        pg.click(pg.center(cor_end_turn), duration=0.2)
        sleep(5, QT)
    elif cor_start != None:
        pg.click(pg.center(cor_start), duration=0.2)
        sleep(5, QT)
        while pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi) == None:
            sleep(0.5, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                return
        pg.click(pg.locateCenterOnScreen(img_confirm, grayscale=True, confidence=confi), duration=0.5)
        sleep(2, QT)
        
    elif cor_traditional_game != None:
        pg.click(pg.center(cor_traditional_game), duration=0.2)
        sleep(2, QT)

    elif pg.locate(img_loss, screenshotIm, grayscale=True, confidence=confi) != None:
        var['loss'] += 1
        logger.info('loss; win: %i; loss: %i', var['win'], var['loss'])
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(waiting_pos, duration=0.2)
            sleep(1, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return
    elif pg.locate(img_win, screenshotIm, grayscale=True, confidence=confi) != None:
        var['win'] += 1
        logger.info('win; win: %i; loss: %i', var['win'], var['loss'])
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(waiting_pos, duration=0.2)
            sleep(1, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return

def isRealWindow(hWnd) -> bool:
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowSizes() -> list:
    '''
    Return a list of tuples (handler, rect) for each real window.
    Rect is a tuple of (left, top, right, button)
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        windows.append((hWnd, rect))
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def get_hwnds_for_pid (pid):
    def callback (hwnd, hwnds):
        if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
            if found_pid == pid:
                hwnds.append (hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def checkIfProcessRunning(processName:str, kill=False):
    '''Return the process id if it is running or return None'''
    call = 'TASKLIST', '/FI', 'imagename eq %s' % processName
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
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
    
def update_stats(logger: logging.Logger=None):
    rows = []
    with open('dist/stats.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    if var['win']+var['loss'] != 0:
        logger.info('win: %i; loss: %i; error: %i; win rate: %.4f',
            var['win'], var['loss'], var['error'], var['win']/(var['win']+var['loss']))
        rows.append([str(var[a]) for a in var])
        with open('dist/stats.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvwriter.writerows(rows)
    wins, losses = 0, 0
    for row in rows:
        wins += int(row[0])
        losses += int(row[1])
    if logger is not None:
        logger.info('total wins: %i, losses: %i, win rate: %.4f'%(wins, losses, wins/(wins+losses)))
    return

if __name__ == '__main__':
    log_file_start = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
    logger = logger_init(log_file_start)
    
    var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
    state = 0

    screensize = pg.size()
    waiting_pos = (screensize[0]/2, screensize[1]*0.75)
    game_window = default_game_window
    pid = checkIfProcessRunning("Hearthstone.exe")
    if pid is None:
        error_state(var, logger)
        pid = checkIfProcessRunning("Hearthstone.exe")
    if pid is not None:
        hwnds = get_hwnds_for_pid(pid)
        wins = getWindowSizes()
        if len(hwnds) != 0:
            for win in wins:
                if hwnds[0] == win[0]:
                    game_window = win[1]
                    break
    logger.info('game window: (%i, %i, %i, %i)'%(game_window))
    # regions = (left, top, width, height)
    cards = (game_window[0]+650, game_window[1]+970, 600, 50)
    minions = (game_window[0]+380, game_window[1]+530, 1050, 30)
    enemy_minions = (game_window[0]+420, game_window[1]+345, 1020, 30)
    hero = (game_window[0]+780, game_window[1]+800, 460, 30)
    enemy_hero = (game_window[0]+922, game_window[1]+153)
    waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)

    logger.info("script starts")
    while keyboard.is_pressed('q') == False:
        try:
            state = check_state(var, state)
            logger.info('state: %i', state)
            if state == 0:
                out_game(var)
            elif state == 1:
                my_turn()
            elif state == 2:
                sleep(1)
            elif state == 3:
                error_state(var, logger)
                var['timestamp'] = datetime.now()
        except (KeyboardInterrupt, pg.FailSafeException):
            break
        except OSError:
            logger.info(traceback.format_exc())
            continue
        except:
            logger.info(traceback.format_exc())
            try:
                error_state(var, logger)
                var['timestamp'] = datetime.now()
            except:
                logger.info(traceback.format_exc())
                break
    
    logger.info("script ends")
    update_stats(logger)
    logger_deconstruct(logger, log_file_start)
