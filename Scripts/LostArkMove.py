from pickle import TRUE
import mouse
import time
import pygetwindow as gw
from pynput.keyboard import Key, Controller
import pyautogui

while TRUE:
    keyboard = Controller()
    win = gw.getWindowsWithTitle('World of Warcraft')[0]
    win.activate()
    mouse.move("1000", "500")
    keyboard.press('w')
    time.sleep(1)
    keyboard.release('w')
    keyboard.press('a')
    time.sleep(1)
    keyboard.release('a')
    
    keyboard.press(Key.space)
    time.sleep(0.5)
    keyboard.release(Key.space)
    mouse.click(button='left')
    time.sleep(0.5)
    mouse.click('middle')
    time.sleep(0.5)
    mouse.click('middle')
    pyautogui.dragTo(300, 400, 2, button='right')
    pyautogui.dragTo(300, 400, 2, button='left')
    print("ping")
    time.sleep(600)
    keyboard.press('s')
    time.sleep(1)
    keyboard.release('s')
    keyboard.press('d')
    time.sleep(1)
    keyboard.release('d')
    time.sleep(0.5)
    mouse.click('middle')
    time.sleep(0.5)
    mouse.click('middle')
    time.sleep(60)
    