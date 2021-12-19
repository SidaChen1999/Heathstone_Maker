import pyautogui as pg
import pyautogui
import time
import keyboard
import random
import win32api, win32con

time.sleep(2)

def click(x,y):
    # win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def tuple_add(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i + j, a, b))
def tuple_sub(a:tuple, b:tuple):
    return tuple(map(lambda i, j: i - j, a, b))
def tuple_abs_sum(a:tuple):
    return sum([abs(number) for number in a])
epsilon = 50

target = (25, 201, 208)
top_left_X = 979
top_left_Y = 368
bottom_right_X = 1579
bottom_right_Y = 790
middle = (2560/2, 1440/2)

while keyboard.is_pressed('s') == False:
    time.sleep(0.05)

print("script starts")

while keyboard.is_pressed('q') == False:
    flag = 0
    pic = pyautogui.screenshot(region=(middle[0]-500 , middle[1]-500, middle[0]+500, middle[1]+500))
    width, height = pic.size

    for x in range(0, width, 10):
        for y in range(0, height, 10):
            color = pic.getpixel((x, y))
            if tuple_abs_sum(tuple_sub(color, target)) < epsilon:
                flag = 1
                # if  x-500+50 < 40 or  x-500+50 < 40:
                #     pass
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x-500+50, y-500+50, 0, 0)
                click(x+middle[0]-500, y+middle[1]-500)
                time.sleep(0.1)
                # print('x, y: ', x-500+40, ' ', y-500+40)
                break

        if flag == 1:
            break
print("script ends")