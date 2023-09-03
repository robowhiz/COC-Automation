import cv2
import pyautogui
import time
import numpy as np
from PIL import ImageGrab
import easyocr

reader = easyocr.Reader(['en'], gpu = True) #loading easy ocr reader

def take_screenshot():
    time.sleep(0.1)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img 

def collect_Rewards():
    img = take_screenshot()

    if img[980][270][0] == 32 and img[980][270][1] == 21 and img[980][270][2] == 241:
        pyautogui.click(x = 240, y = 1010)
        time.sleep(1)
        pyautogui.click(x = 1000, y = 50)
        time.sleep(1)
    
        img = take_screenshot()

        cropped_img = img[9:40, 1141:1173]
        cropped_img = cv2.resize(cropped_img, (93, 96))

        count = reader.readtext(cropped_img, allowlist = "1234567890", detail = 0)
        if len(count) == 0:
            pyautogui.click(x = 1630, y = 50)
            return

        for x in range(int(count[0])):
            pyautogui.click(x = 1580, y = 620)
            time.sleep(1)
            pyautogui.click(x = 340, y = 620)
            time.sleep(1)
            pyautogui.click(x = 960, y = 855)
            time.sleep(1)
        
        pyautogui.click(x = 1630, y = 50)
        time.sleep(1)