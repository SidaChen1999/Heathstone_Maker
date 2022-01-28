import pyautogui as pg
import keyboard
pic = 'pics/pic_piano.jpg'
while keyboard.is_pressed('s') == False:
    pg.sleep(0.1)
print("script starts")
region = (640,720,640,160)
# print(pg.screenshot(region=region).getpixel((0,0)))

cnt = 1
import win32api, win32con
def click(cor):
    win32api.SetCursorPos(cor)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cor[0], cor[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cor[0], cor[1], 0, 0)

while keyboard.is_pressed('q') == False:
    pic = pg.screenshot(region=region)
    # if pic.getpixel((0, 0)) != (184,223,230):
    #     continue
        # print(pic.getpixel((0, 0)))
    for i in range(4):
        if pic.getpixel((i*160+80, 80)) != (255,255,255):
            click((i*160+80+642, 80+721))
            # print(cnt)
            # cnt += 1
            pg.sleep(0.015)
            break