import pyautogui
import time
import os

import random
time.sleep(5)
while(1):
    num=random.randint(1,4)
    if(num==1):
        pyautogui.press('right',presses=1,interval=0.3)
    if(num==2):
        pyautogui.press('left',presses=1,interval=0.3)
    if(num==3):
        pyautogui.press('up',presses=1,interval=0.3)
    if(num==4):
        pyautogui.press('down',presses=1,interval=0.3)
    a=random.randint(0,5)
    time.sleep(a)
