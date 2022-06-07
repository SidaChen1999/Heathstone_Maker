import keyboard
import pyautogui as pg

SLEEP = 1.5
while keyboard.is_pressed('s') == False:
    print('waiting')
    pg.sleep(0.1)
cnt = 0
while keyboard.is_pressed('space') == False:
    pg.click(950, 700) # card
    pg.sleep(SLEEP)
    pg.click(1127, 474) # summon ability
    pg.sleep(SLEEP)
    pg.click(1519, 483) # end
    pg.sleep(6)
    pg.click(950, 700) # card
    pg.sleep(SLEEP)
    pg.click(785, 474) # kill ability
    pg.sleep(SLEEP)
    pg.click(884, 307) # point to enemy
    pg.sleep(SLEEP)
    pg.click(1519, 483) # end
    pg.sleep(10)
    cnt = cnt + 1
    print('Counted: ', cnt)
      
print('ends')