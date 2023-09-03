import cv2
import numpy as np
import pyautogui
import time
from PIL import ImageGrab

def take_screenshot():
    time.sleep(0.5)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def collect_resources(x, y):
    def treasury():
        img = take_screenshot()
        template = cv2.imread("templates\\resources\\5.png")

        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) > 0.7)
        if coordinates[0].size > 0:
            pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])
            
            img = take_screenshot()
            template = cv2.imread("templates\\resources\\6.png")

            coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) > 0.85)
            if coordinates[0].size > 0:
                pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])
                time.sleep(0.5)
                pyautogui.click(x = 970, y = 740)
                time.sleep(0.5)
                pyautogui.click(x = 1100, y = 650)
                time.sleep(0.5)
                pyautogui.click(x = 1860, y = 500, clicks = 2, interval = 0.5)
        
    if y != 0:
        for z in range(x, y + 1):
            if z == 5:
                treasury()
                continue
            
            img = take_screenshot()
            template = cv2.imread('templates\\resources\\' + str(z) + '.png')

            coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.7)
            if coordinates[0].size > 0:
                pyautogui.click(x = coordinates[1][0] + 5, y = coordinates[0][0] + 5) #clicking on image
                if z == 4:
                    time.sleep(1)
                    pyautogui.click(x = 940, y = 850)
            time.sleep(2)

    else:
        if x == 5:
            treasury()
            return
        
        img = take_screenshot()
        template = cv2.imread('templates\\resources\\' + str(x) + '.png')

        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.7)
        if coordinates[0].size > 0:
            pyautogui.click(x = coordinates[1][0] + 5, y = coordinates[0][0] + 5) #clicking on image
        time.sleep(1)

collect_resources(1,2)