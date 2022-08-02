import logging
import traceback
import keyboard
import pyautogui as pg
from parameters import *
from datetime import datetime
from util import GetWindowRectFromName, check_state_merc, end_turn, error_state, \
    event, find_color, logger_deconstruct, logger_init, setWindow, sleep, update_stats

def my_turn(param:param):
    pic_cards = pg.screenshot('test_pics/cards.jpg', region=param.cards)
    pic_mercenary_ability = pg.screenshot('test_pics/mercenary_ability.jpg', region=param.mercenary_ability)

    x_cards, y_cards = find_color(pic_cards, 2, epsilon, green)
    if x_cards is not None:
        pg.click(x_cards+param.cards[0], y_cards+param.cards[1]+20, duration=0.2)
        pg.click(param.enemy_hero, clicks=2, interval=0.5, duration=0.2)

    x_minions, y_minions = find_color(pic_mercenary_ability, 5, epsilon, green, green2, yellow)
    if x_minions is not None:
        pg.click(x_minions+param.mercenary_ability[0], y_minions+param.mercenary_ability[1]+40, duration=0.2)
        pic_enemy_minions = pg.screenshot('test_pics/enemy_mercenary.jpg', region=param.enemy_mercenary)
        x_enemy, y_enemy = find_color(pic_enemy_minions, 5, epsilon, red)
        if x_enemy is not None:
            pg.click(x_enemy+param.enemy_mercenary[0], y_enemy+param.enemy_mercenary[1], duration=0.2)
        else:
            pg.click(param.default_mercenary, duration=0.2)
    pg.click(param.enemy_hero, clicks=1, interval=0.2, button='RIGHT', duration=0.2)

    if x_minions is None and x_cards is None:
        cor_buble = pg.locateOnScreen(img_buble, grayscale=True, confidence=confi)
        if cor_buble is not None:
            point = pg.center(cor_buble)
            pg.click(point[0]-40, point[1]+80, duration=0.2)

def out_game(var, param:param, logger: logging.Logger=None, QT:bool=None):
    screenshotIm = pg.screenshot()
    cor_merc_start = pg.locate(img_merc_start, screenshotIm, grayscale=True, confidence=confi)
    cor_mercenary = pg.locate(img_mercenary, screenshotIm, grayscale=True, confidence=confi)
    cor_travel_point = pg.locate(img_travel_point, screenshotIm, grayscale=True, confidence=0.6)
    cor_select_travel = pg.locate(img_select_travel, screenshotIm, grayscale=True, confidence=confi)
    cor_select_level = pg.locate(img_select_level, screenshotIm, grayscale=True, confidence=0.6)
    cor_lock = pg.locate(img_lock, screenshotIm, grayscale=True, confidence=confi)
    cor_fight = pg.locate(img_fight, screenshotIm, grayscale=True, confidence=confi)
    cor_proceed = pg.locate(img_proceed, screenshotIm, grayscale=True, confidence=confi)
    cor_victory = pg.locate(img_victory, screenshotIm, grayscale=True, confidence=confi)
    cor_treasure = pg.locate(img_treasure, screenshotIm, grayscale=True, confidence=confi)
    cor_merc_level = pg.locate(img_mercenary_level, screenshotIm, grayscale=True, confidence=confi)
    cor_open_treasure = pg.locate(img_open_treasure, screenshotIm, grayscale=False, confidence=0.9)
    cor_finish = pg.locate(img_finish, screenshotIm, grayscale=False, confidence=0.6)
    cor_merc_confirm = pg.locate(img_merc_confirm, screenshotIm, grayscale=True, confidence=confi)
    cor_select_treasure = pg.locate(img_select_treasure, screenshotIm, grayscale=True, confidence=confi)
    cor_campfire = pg.locate(img_campfire, screenshotIm, grayscale=True, confidence=confi)
    cor_jump = pg.locate(img_jump, screenshotIm, grayscale=True, confidence=confi)
    cor_pickup = pg.locate(img_pickup, screenshotIm, grayscale=True, confidence=confi)
    cor_reveal = pg.locate(img_reveal, screenshotIm, grayscale=True, confidence=confi)

    if cor_merc_start != None:
        pg.click(pg.center(cor_merc_start), duration=0.2)
        print("merc start")
        sleep(1, QT)
    elif cor_mercenary != None:
        pg.click(pg.center(cor_mercenary), duration=0.2)
        print("mercenary")
        sleep(3, QT)
    elif cor_travel_point != None:
        pg.click(pg.center(cor_travel_point), duration=0.2)
        print("travel point")
        sleep(1, QT)
    elif cor_select_travel != None:
        print("merc select travel")
        pg.click(pg.center(cor_select_travel), duration=0.2)
        sleep(1, QT)
    elif cor_lock != None:
        print("merc lock")
        pg.click(pg.center(cor_lock), duration=0.2)
        sleep(1, QT)
    elif cor_select_level != None:
        print("merc select level")
        pg.click(pg.center(cor_select_level), duration=0.2)
        sleep(2, QT)
    elif cor_fight != None:
        print("merc fight")
        pg.click(pg.center(cor_fight), duration=0.2)
        sleep(1, QT)
    elif cor_proceed != None:
        print("merc proceed")
        pg.click(pg.center(cor_proceed), duration=0.2)
        sleep(1, QT)
    elif cor_treasure != None:
        print("merc treasure")
        pg.click(pg.center(cor_treasure), duration=0.2)
        sleep(1, QT)
    elif cor_merc_level != None:
        print("merc choose level")
        pg.click(pg.center(cor_merc_level), duration=0.2)
        sleep(1, QT)
    elif cor_victory != None:
        print("merc victory")
        var['win'] += 1
        if logger is None:
            print('level; levels: %i; rounds: %i' % (var['win'], var['loss']))
        else:
            logger.info('level; levels: %i; rounds: %i' % (var['win'], var['loss']))
        pg.click((game_window[0]+game_window[2])/2, (game_window[1]+game_window[3])/2, duration=0.2)
        while True:
            cor_acquire = pg.locateOnScreen(img_acquire, grayscale=True, confidence=0.6)
            cor_open_treasure = pg.locateOnScreen(img_open_treasure, grayscale=False, confidence=0.9)
            print("acquire: ", cor_acquire, "; open treasure: ", cor_open_treasure)
            if cor_acquire != None or cor_open_treasure != None:
                break
            if event.is_set():
                return
            pg.click(param.merc_waiting_pos, duration=0.2)
            pg.click(param.mid_point, duration=0.2)
            sleep(0.5, QT)
            if (datetime.now() - var['timestamp']).seconds > timeout:
                    return
        if cor_acquire != None:
            pg.click(cor_acquire, duration=0.2)
            sleep(2, QT)
            pg.click(param.merc_waiting_pos, duration=0.2)
        sleep(0.5, QT)
    elif cor_open_treasure != None:
        print("merc opened treasure")
        open_treasure(var, param, logger, QT)
    elif cor_finish != None:
        print("merc open treasure finish")
        pg.click(pg.center(cor_finish), duration=0.2)
        pg.click(param.merc_waiting_pos, button='RIGHT', duration=0.2)
        sleep(1, QT)
        pg.click(param.merc_waiting_pos, duration=0.2)
    elif cor_merc_confirm != None:
        print("merc confirm")
        var['loss'] += 1
        if logger is None:
            print('level; levels: %i; rounds: %i' % (var['win'], var['loss']))
        else:
            logger.info('level; levels: %i; rounds: %i' % (var['win'], var['loss']))
        pg.click(pg.center(cor_merc_confirm), duration=0.2)
        sleep(1, QT)
    elif pg.locate(img_no_enemy, screenshotIm, grayscale=True, confidence=confi) != None:
        print("merc find enemy")
        pic_enemy_region = pg.screenshot('test_pics/enemy_region.jpg', region=param.enemy_region)
        x_enemy, y_enemy = find_color(pic_enemy_region, 2, 10, green, green2, merc_green)
        print("Enemy at: ", (x_enemy, y_enemy))
        if x_enemy is not None:
            pg.mouseDown(x_enemy+param.enemy_region[0], 
                y_enemy+param.enemy_region[1]+20, duration=0.2)
            sleep(0.1, QT)
            pg.mouseUp()
            # pg.click(x_enemy+param.enemy_region[0], y_enemy+param.enemy_region[1]+20,
            #     clicks=2, interval=0.5, duration=0.2)
            pg.click(param.merc_waiting_pos, duration=0.2)
    elif cor_select_treasure != None:
        print("merc select treasure")
        pg.click(param.mid_point, duration=0.2)
        if pg.locateOnScreen(img_acquire, grayscale=True, confidence=0.6) != None:
            pg.click(pg.locateOnScreen(img_acquire, grayscale=True, confidence=0.6), duration=0.2)
    elif cor_campfire != None:
        print("merc mission")
        pic_mission_region = pg.screenshot('test_pics/mission_region.jpg', region=param.treasure_region)
        x_mission, y_mission = find_color(pic_mission_region, 2, 10, blue)
        print("mission at: ", (x_mission, y_mission))
        if x_mission is not None:
            pg.click(x_mission+param.treasure_region[0]+20, y_mission+param.treasure_region[1], duration=0.2)
            sleep(1, QT)
            if pg.locateOnScreen(img_receive, grayscale=True, confidence=confi) == None:
                pg.click(param.merc_waiting_pos, duration=0.2)
            else:
                pg.click(pg.locateOnScreen(img_receive, grayscale=True, confidence=confi), duration=0.2)
                while pg.locateOnScreen(img_campfire, grayscale=True, confidence=confi) == None:
                    pg.click(param.mid_point, duration=0.2)
                    if event.is_set():
                        return
                    if (datetime.now() - var['timestamp']).seconds > timeout:
                            return
                    sleep(0.5, QT)
        else:
            pg.click(param.merc_waiting_pos, duration=0.2)
    elif cor_jump != None:
        print("merc jump")
        pg.click(pg.center(cor_jump), duration=0.2)
        sleep(1, QT)
    elif cor_pickup != None:
        print("merc pick up")
        pg.click(pg.center(cor_pickup), clicks=2, interval=0.5, duration=0.2)
        sleep(1, QT)
    elif cor_reveal != None:
        print("merc reveal")
        pg.click(pg.center(cor_reveal), clicks=2, interval=0.5, duration=0.2)
        sleep(1, QT)
    # pg.click(param.merc_waiting_pos, duration=0.2)
    # pg.click(param.merc_waiting_pos, button='RIGHT', duration=0.2)

def open_treasure(var, param:param, logger: logging.Logger=None, QT:bool=None):
    pic_treasure_region = pg.screenshot('test_pics/treasure_region.jpg', region=param.treasure_region)
    x_treasure, y_treasure = find_color(pic_treasure_region, 2, 10, gold)
    print("treasure at: ", (x_treasure, y_treasure))
    if x_treasure is not None:
        pg.click(x_treasure+param.treasure_region[0], y_treasure+param.treasure_region[1], duration=0.2)
        pg.click(param.merc_waiting_pos, duration=0.2)

if __name__ == '__main__':
    log_file_start = 'log/'+datetime.now().strftime("%Y-%m-%d,%H-%M-%S")+'.log'
    logger = logger_init(log_file_start)
    
    var = {'win': 0, 'loss': 0, 'error': 0, 'timestamp': datetime.now(), 'rounds': 0}
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

    logger.info("script starts")
    while keyboard.is_pressed('q') == False:
        try:
            state = check_state_merc(var, params, state)
            logger.info('state: %i' % state)
            if state == 0:
                out_game(var, params, logger)
            elif state == 1:
                # my_turn(params)
                pass
            elif state == 2:
                sleep(1)
            elif state == 3:
                error_state(var, params, logger, merc=True)
                var['timestamp'] = datetime.now()
            elif state == 4:
                end_turn(params)
        except (KeyboardInterrupt, pg.FailSafeException):
            break
        except OSError:
            logger.error(traceback.format_exc())
            continue
        except:
            logger.info(traceback.format_exc())
            try:
                error_state(var, params, logger, merc=True)
                var['timestamp'] = datetime.now()
            except:
                logger.info(traceback.format_exc())
                break
    
    logger.info("script ends")
    update_stats(var, logger, False)
    logger_deconstruct(logger, log_file_start)