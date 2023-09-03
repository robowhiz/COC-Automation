import cv2
import numpy as np
import pyautogui
import time
from PIL import ImageGrab
import easyocr

reader = easyocr.Reader(['en'], gpu = True) #loading easy ocr reader

def take_screenshot():
    time.sleep(0.1)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img 

def train_army():
    pyautogui.click(x = 60, y = 830) #clicking on the train troop button
    time.sleep(1)
    pyautogui.click(x = 650, y = 145) #clicking on the train button
    time.sleep(0.5)
    pyautogui.click(x = 850, y = 635, clicks = 10, interval = 0.1) #clicing on wizard 10 times to add to the training queue
    time.sleep(0.5)
    
    img = take_screenshot()
    img = cv2.resize(img[265:300,1460:1535], (160,70))
    clicks = int(int(reader.readtext(img, allowlist = "0123456789", detail = 0)[0])/5) * 2
    
    pyautogui.click(x = 700, y = 800, clicks = clicks, interval = 0.1)
    time.sleep(1)
    pyautogui.click(x = 850, y = 635, clicks = 10, interval = 0.1) #clicking on the wizard 10 times
    time.sleep(0.5)
    pyautogui.click(x = 900, y = 145) #clicking on brew spell button
    time.sleep(0.5)
    pyautogui.mouseDown(x = 360, y = 640) #long pressing on lightning spell for 3 seconds
    time.sleep(3)
    pyautogui.mouseUp()
    time.sleep(0.5)
    pyautogui.click(x = 1860, y = 500) #clicking on the edge of the screen to come back to home screen

def train_rest():
    time.sleep(1)
    pyautogui.click(x = 60, y = 830) #clicking on the train troop button
    time.sleep(1)
    pyautogui.click(x = 650, y = 145) #clicking on the train button
    time.sleep(0.5)
    pyautogui.mouseDown(x = 700, y = 800)
    time.sleep(2)
    pyautogui.mouseUp()
    time.sleep(0.5)
    pyautogui.click(x = 1860, y = 500) #clicking on the edge of the screen to come back to home screen
    time.sleep(2)

train_rest()
train_army()