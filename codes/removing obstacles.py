import cv2
import numpy as np
import pyautogui
import time 
import os
from PIL import ImageGrab

def take_screenshot():
    time.sleep(0.5)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def builder_availability(): #check the builder is avialable or not
    img = take_screenshot() #taking the screenshot of the home screen
    template = cv2.imread('templates\\builder.png') #loading the "0/" image
    
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)
    if coordinates[0].size > 0: #"0/" image found
        return 0 #no builder is available
    
    else: #"0/" image not found
        return 1 #atleast one builder is available

def remove_obstacles():
    lst = os.listdir("templates\\removing obstacles")
    obstbles_count = len(lst)
    
    obstacle_number = 1
    while obstacle_number <= obstbles_count:
        img = take_screenshot()

        template = cv2.imread('templates\\removing obstacles\\' + str(obstacle_number) + '.png')

        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)
        if coordinates[0].size > 0:
            for x in range(coordinates[0].size):
                if coordinates[0][x] > 120:
                    pyautogui.click(x = coordinates[1][x] + 5, y = coordinates[0][x] + 5)
                    time.sleep(0.5)
                    pyautogui.click(x = 960, y = 900)
                    time.sleep(0.5)
                    pyautogui.click(x = 1860, y = 500)
                    time.sleep(12)
                    break

            if coordinates[0][x] < 120:
                obstacle_number += 1

        else :
            obstacle_number += 1

if builder_availability() == 1:
    remove_obstacles()