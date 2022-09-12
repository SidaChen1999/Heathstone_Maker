import pyautogui as pg
import keyboard
from datetime import datetime
import logging
import traceback
from parameters import *
from util import GetWindowRectFromName, check_state, end_turn, error_state, \
    find_color, log, logger_deconstruct, logger_init, setWindow, sleep, event, update_stats

def my_turn(param:param):
    pic_cards = pg.screenshot('test_pics/cards.jpg', region=param.cards)
    pic_minions = pg.screenshot('test_pics/minions.jpg', region=param.minions)
    pic_hero = pg.screenshot('test_pics/hero.jpg', region=param.hero)

    x_cards, y_cards = find_color(pic_cards, 2, epsilon, yellow, green)
    if x_cards is not None:
        pg.click(x_cards+param.cards[0], y_cards+param.cards[1]+20, duration=0.2)
        pg.click(param.enemy_hero, clicks=2, interval=0.5, duration=0.2)

    x_minions, y_minions = find_color(pic_minions, 5, epsilon, green, green2)
    if x_minions is not None:
        pg.click(x_minions+param.minions[0], y_minions+param.minions[1]+40, duration=0.2)
        enemy_hero_color = pg.pixel(param.enemy_hero[0], param.enemy_hero[1])
        if enemy_hero_color[0]>235 and enemy_hero_color[1]>235 and enemy_hero_color[2]<235:
            pg.click(param.enemy_hero, duration=0.2)
        else:
            pic_enemy_minions = pg.screenshot('test_pics/enemy_minions.jpg', region=param.enemy_minions)
            x_enemy, y_enemy = find_color(pic_enemy_minions, 5, epsilon, red)
            if x_enemy is not None:
                pg.click(x_enemy+param.enemy_minions[0]+20, y_enemy+param.enemy_minions[1]+40, duration=0.2)
            else:
                pg.click(param.enemy_hero, duration=0.2)

    if x_minions is None and x_cards is None:
        x_hero, y_hero = find_color(pic_hero, 3, epsilon, green)
        if x_hero is not None:
            pg.click(x_hero+param.hero[0], y_hero+param.hero[1]+30, duration=0.2)
            pg.click(param.enemy_hero, duration=0.2)
    pg.click(param.enemy_hero, clicks=1, interval=0.2, button='RIGHT', duration=0.2)

def out_game(var, param:param, logger: logging.Logger=None, QT:bool=None):
    screenshotIm = pg.screenshot()
    cor_start = pg.locate(img_start, screenshotIm, grayscale=True, confidence=confi)
    cor_traditional_game = pg.locate(img_traditional_game, screenshotIm, grayscale=True, confidence=confi)
    cor_close = pg.locate(img_close, screenshotIm, grayscale=True, confidence=confi)
    if cor_start != None:
        pg.click(pg.center(cor_start), duration=0.2)
        sleep(5, QT)
        while pg.locateOnScreen(img_confirm, grayscale=True, confidence=confi) == None:
            if event.is_set():
                return
            sleep(1, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                return
        pg.click(pg.locateCenterOnScreen(img_confirm, grayscale=True, confidence=confi), duration=0.2)
        sleep(2, QT)
        
    elif cor_traditional_game != None:
        pg.click(pg.center(cor_traditional_game), duration=0.2)
        sleep(2, QT)
    elif cor_close != None:
        pg.click(pg.center(cor_close), duration=0.2)
        sleep(1, QT)

    elif pg.locate(img_loss, screenshotIm, grayscale=True, confidence=confi) != None:
        var['loss'] += 1
        log('loss; win: %i; loss: %i' % (var['win'], var['loss']), logger)
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            if event.is_set():
                return
            pg.click(param.waiting_pos, duration=0.2)
            sleep(1, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return
    elif pg.locate(img_win, screenshotIm, grayscale=True, confidence=confi) != None:
        var['win'] += 1
        log('win; win: %i; loss: %i' % (var['win'], var['loss']), logger)
        while pg.locateOnScreen(img_start, grayscale=False, confidence=confi) == None:
            if event.is_set():
                return
            pg.click(param.waiting_pos, duration=0.2)
            sleep(1, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return

counter = 0
def surrender(logger: logging.Logger=None):
    global counter
    counter += 1
    log("Surrendered %i times" % counter, logger)
    keyboard.send("esc")
    sleep(0.5)
    cor_surrender = pg.locateCenterOnScreen(img_surrender, grayscale=True, confidence=confi)
    if cor_surrender != None:
        pg.click(cor_surrender, duration=0.2)
    else:
        keyboard.send("esc")
    sleep(1)

if __name__ == '__main__':
    log_file_start = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
    logger = logger_init(log_file_start)
    
    var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now()}
    state = 0

    params = param()
    rect = GetWindowRectFromName(hwnd_name)
    if rect is None:
        error_state(var, params, logger)
        rect = GetWindowRectFromName(hwnd_name)
    else:
        setWindow(hwnd_name, game_window)
        rect = GetWindowRectFromName(hwnd_name)
    if rect is not None:
        logger.info('game window: (%i, %i, %i, %i)' % rect)

    waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)

    logger.info("script starts")
    while keyboard.is_pressed('q') == False:
        try:
            state = check_state(var, state)
            logger.info('state: %i' % state)
            if state == 0:
                out_game(var, params, logger)
            elif state == 1:
                my_turn(params)
            elif state == 2:
                sleep(1)
            elif state == 3:
                error_state(var, params, logger)
                var['timestamp'] = datetime.now()
            elif state == 4:
                end_turn(params)
            elif state == 5:
                surrender(logger)
        except (KeyboardInterrupt, pg.FailSafeException):
            break
        except OSError:
            logger.error(traceback.format_exc())
            continue
        except:
            logger.info(traceback.format_exc())
            try:
                error_state(var, params, logger)
                var['timestamp'] = datetime.now()
            except:
                logger.info(traceback.format_exc())
                break
    
    logger.info("script ends")
    update_stats(var, logger)
    logger_deconstruct(logger, log_file_start)
