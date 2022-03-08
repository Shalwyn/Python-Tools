from pickle import TRUE
import mouse
import time
import pygetwindow as gw

while TRUE:
    win = gw.getWindowsWithTitle('LOST ARK')[0]
    win.activate()
    mouse.move("1000", "500")
    mouse.click(button='left')
    print("ping")
    time.sleep(600)
    