from pyautogui import *
import pyautogui
import time
import random
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    