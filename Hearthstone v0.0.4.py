#!/usr/bin/env python
import pyautogui as pg
import keyboard
import psutil
from datetime import datetime
import csv
import logging
import traceback
import win32con
import win32gui
import win32process
import os
from parameters import *

def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
def delta(a, b):
    return tuple_abs_sum(tuple_sub(a, b))

def check_state(var, last_state, simple=False):
    cor_enemy_turn = pg.locateOnScreen(img_enemy_turn, grayscale=False, confidence=confi)
    cor_my_turn = pg.locateOnScreen(img_my_turn, grayscale=False, confidence=confi)
    cor_my_turn1 = pg.locateOnScreen(img_my_turn1, grayscale=False, confidence=confi)
    if cor_enemy_turn != None:
        next_state = 2
    elif cor_my_turn != None:
        next_state = 1
    elif cor_my_turn1 != None:
        next_state = 1
    else:
        next_state = 0
    if simple:
        return next_state
    if last_state == next_state:
        if (datetime.now() - var['timestamp']).seconds > timeout:
            var['timestamp'] = datetime.now()
            error_state(var, logger)
            var['timestamp'] = datetime.now()
    else:
        var['timestamp'] = datetime.now()
    return next_state

def error_state(var, logger: logging.Logger):
    var['error'] += 1
    logger.error('error: %i', var['error'])
    cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_play != None:
        pg.click(cor_play, duration=0.5)
        pg.sleep(10)
    else:
        proc = checkIfProcessRunning('hearthstone', kill=True)
        pg.sleep(2)
        if proc == None:
            cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
            if cor_battlenet != None:
                pg.click(cor_battlenet, duration=0.5)
                pg.sleep(1)
            else:
                return
        else:
            cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
            if cor_play == None:
                cor_battlenet = pg.locateCenterOnScreen(img_battlenet, grayscale=True, confidence=confi)
                if cor_battlenet != None:
                    pg.click(cor_battlenet, duration=0.5)
                    pg.sleep(1)
                else:
                    return
        cor_play = pg.locateCenterOnScreen(img_play, grayscale=True, confidence=confi)
        if cor_play != None:
            var['timestamp'] = datetime.now()
            pg.click(cor_play, duration=0.5)
            pg.sleep(10)
    while pg.locateCenterOnScreen(img_traditional_game, grayscale=True, confidence=confi) == None:
        pg.sleep(2)
        pg.click(waiting_pos, duration=0.3)
        if check_state(var, state, simple=True) != 0:
            break
        if (datetime.now() - var['timestamp']).seconds > timeout:
            return

last_minion = 0
last_card = 0
def my_turn(last_minion, last_card):
    pic_cards = pg.screenshot('test_pics/cards.jpg', region=cards)
    pic_minions = pg.screenshot('test_pics/minions.jpg', region=minions)
    
    width, height = pic_cards.size
    flag = 0
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            color = pic_cards.getpixel((x, y))
            if delta(color, green) < epsilon or delta(color, yellow) < epsilon:
                flag = 1
                if last_card != x:
                    pg.click(x+cards[0]+20, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                else:
                    pg.click(x+cards[0]-20, y+cards[1], duration=0.3)
                    pg.click(enemy_hero, clicks=2, interval=0.5, duration=0.3)
                last_card = x
                break
        if flag == 1:
            break

    width, height = pic_minions.size
    flag = 0
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            color = pic_minions.getpixel((x, y))
            if delta(color, green) < epsilon or delta(color, green2) < epsilon:
                flag = 1
                if last_minion != x:
                    pg.click(x+minions[0]+20, y+minions[1]+40, duration=0.3)
                else:
                    pg.click(x+minions[0]-20, y+minions[1]+40, duration=0.3)
                last_minion = x
                # overcome wall
                target_color = pg.pixel(enemy_hero[0], enemy_hero[1])
                if delta(target_color, red) < epsilon+20:
                    pg.click(enemy_hero, duration=0.3)
                else:
                    pic_enemy_minions = pg.screenshot('test_pics/enemy_minions.jpg', region=enemy_minions)
                    enemy_width, enemy_height = pic_enemy_minions.size
                    enemy_flag = 0
                    for i in range (0, enemy_width, 5):
                        for j in range (0, enemy_height, 5):
                            enemy_color = pic_enemy_minions.getpixel((i, j))
                            if delta(enemy_color, red) < epsilon:
                                enemy_flag = 1
                                pg.click(i+enemy_minions[0], j+enemy_minions[1]+40, duration=0.3)
                        if enemy_flag == 1:
                            break
                break
        if flag == 1:
            return

    pic_hero = pg.screenshot('test_pics/hero.jpg', region=hero)
    width, height = pic_hero.size
    flag = 0
    for x in range(0, width, 3):
        for y in range(0, height, 3):
            color = pic_hero.getpixel((x, y))
            if delta(color, green) < epsilon:
                flag = 1
                pg.click(x+hero[0]+10, y+hero[1], duration=0.3)
                pg.click(enemy_hero, duration=0.3)
                break
        if flag == 1:
            break
    pg.click(waiting_pos, clicks=2, interval=0.2, button='RIGHT', duration=0.2)

def out_game(var):
    cor_start = pg.locateOnScreen(img_start, grayscale=True, confidence=confi)
    cor_traditional_game = pg.locateOnScreen(img_traditional_game, grayscale=True, confidence=confi)
    cor_end_turn = pg.locateOnScreen(img_end_turn, grayscale=False, confidence=confi)
    cor_play = pg.locateOnScreen(img_play, grayscale=True, confidence=confi)
    if cor_end_turn != None:
        x, y = pg.center(cor_end_turn)
        pg.click(x=x,y=y, duration=0.3)
        pg.sleep(5)
    elif cor_start != None:
        x, y = pg.center(cor_start)
        pg.click(x=x,y=y, duration=0.3)
        pg.sleep(5)
        while pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi) == None:
            pg.sleep(0.5)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                return
        x, y = pg.center(pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi))
        pg.click(x=x,y=y, duration=0.5)
        pg.sleep(2)
        
    elif cor_traditional_game != None:
        x, y = pg.center(cor_traditional_game)
        pg.click(x=x,y=y, duration=0.3)
        pg.sleep(2)
    elif cor_play != None:
        error_state(var, logger)
        var['timestamp'] = datetime.now()

    elif pg.locateOnScreen(img_loss, grayscale=True, confidence=confi) != None:
        var['loss'] += 1
        logger.info('w: %i; loss: %i', var['win'], var['loss'])
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(x=waiting_pos[0], y=waiting_pos[1], duration=0.3)
            pg.sleep(1)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return
    elif pg.locateOnScreen(img_win, grayscale=True, confidence=confi) != None:
        var['win'] += 1
        logger.info('win: %i; loss: %i', var['win'], var['loss'])
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            pg.click(x=waiting_pos[0], y=waiting_pos[1], duration=0.3)
            pg.sleep(1)
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

def checkIfProcessRunning(processName, kill=False):
    '''Return the process id if it is running or return None'''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                if kill:
                    proc.kill()
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

if __name__ == '__main__':
    FORMAT = '%(asctime)s %(message)s'
    log_file_start = 'log/'+datetime.now().strftime("%Y-%m-%d,%H%M%S")+'.log'
    logging.basicConfig(filename=log_file_start, format=FORMAT, filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(consoleHandler)
    var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
    state = 0

    screensize = pg.size()
    waiting_pos = (screensize[0]/2, screensize[1]*0.75)
    game_window = default_game_window
    id = checkIfProcessRunning("hearthstone")
    if id is None:
        error_state(var, logger)
        id = checkIfProcessRunning("hearthstone")
    if id is not None:
        hwnds = get_hwnds_for_pid(id)
        wins = getWindowSizes()
        if len(hwnds) != 0:
            for win in wins:
                if hwnds[0] == win[0]:
                    game_window = win[1]
                    break
    logger.info('game window: (%i, %i, %i, %i)'%(game_window))
    # regions = (left, top, width, height)
    cards = (game_window[0]+650, game_window[1]+990, 600, 50)
    minions = (game_window[0]+380, game_window[1]+530, 1050, 30)
    enemy_minions = (game_window[0]+390, game_window[1]+335, 1050, 30)
    hero = (game_window[0]+780, game_window[1]+810, 460, 30)
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
                my_turn(last_minion, last_card)
            elif state == 2:
                pg.sleep(1)
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
    logger.info('total wins: %i, losses: %i, win rate: %.4f'%(wins, losses, wins/(wins+losses)))
    logging.shutdown()
    log_file_end = 'log/'+datetime.now().strftime("%Y-%m-%d,%H%M%S")+'.log'
    os.rename(log_file_start, log_file_end)
