import cv2
import numpy as np
import pyautogui
import time
import os
from PIL import ImageGrab

building_count = 0
search_upgrade_flag = True
new_building_flag = True

def take_screenshot():
    time.sleep(0.5)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def assign_builder():
    lst = os.listdir("templates\\buildings\\search upgrade buildings") #opening the directory of the search upgrade buiding template pictures
    global building_count
    building_count = len(lst) #counting the number of files in that directory

    while builder_availability() == 1: #check builder is available or not
        global search_upgrade_flag, new_building_flag
        if new_building_flag:
            pyautogui.click(x = 730, y = 60) #clicking on the builder icon
            time.sleep(0.5)
            builder_new_building() #new building function
        
        elif search_upgrade_flag: #if all search upgrade building is max go to suggested upgrade
            pyautogui.click(x = 730, y = 60) #clicking on the builder icon
            time.sleep(0.5)
            builder_search_upgrade() #search upgrade building function
            time.sleep(0.5)
            upgrade_button() #pressing the upgrade button
        
        else:
            pyautogui.click(x = 730, y = 60) #clicking on the builder icon
            time.sleep(0.5)
            builder_suggested_upgrade() #suggested building upgrade function
            time.sleep(0.5)
            upgrade_button() #pressing the upgrade button

    pyautogui.click(x = 100, y = 980)
    time.sleep(1)
    pyautogui.click(x = 1380, y = 670)
    time.sleep(2)
    pyautogui.click(x = 100, y = 850)
    time.sleep(0.5)
    pyautogui.click(x = 100, y = 1000)
    time.sleep(5)

def builder_availability(): #check the builder is avialable or not
    img = take_screenshot() #taking the screenshot of the home screen
    template = cv2.imread('templates\\builder.png') #loading the "0/" image
    
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)
    if coordinates[0].size > 0: #"0/" image found
        return 0 #no builder is available
    
    else: #"0/" image not found
        return 1 #atleast one builder is available

def builder_new_building():
    pyautogui.moveTo(x = 800, y = 300)
    time.sleep(0.2)
    pyautogui.scroll(clicks = 500) #scrolling to the top of the upgrade building list
    time.sleep(2)

    template = cv2.imread("templates\\buildings\\new building\\new.png")
    for x in range(1, 6):
        img = take_screenshot()

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        coordinates = np.where(result >= 0.52)
        condition = coordinates[1] < 700
        coordinates = (coordinates[0][condition], coordinates[1][condition])
        builder = np.where(result >= 0.85)
        if coordinates[0].size > 0:
            i = 0
            if builder[0].size > 0:
                for i in range(coordinates[0].size):
                    if abs(builder[0][0] - coordinates[0][i]) > 5:
                        break
            
            if builder[0].size == 0 or abs(builder[0][0] - coordinates[0][i]) > 5:
                pyautogui.click(x = coordinates[1][i] + 10, y = coordinates[0][i] + 5)
                time.sleep(2)

                template = cv2.imread("templates\\buildings\\new building\\arrow.png")
                while True:
                    img = take_screenshot()
                    
                    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.95)
                    
                    if coordinates[0].size > 0:
                        pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])
                        break
                
                time.sleep(1)

                tick_template = cv2.imread("templates\\buildings\\new building\\green tick.png")
                cross_template =  cv2.imread("templates\\buildings\\new building\\red cross.png")
                for y in range(260, 800, 45):
                    for x in range(320, 1580, 45):
                        img = take_screenshot()

                        tick_coordinates = np.where(cv2.matchTemplate(img, tick_template, cv2.TM_CCOEFF_NORMED) >= 0.9)
                        cross_coordinates = np.where(cv2.matchTemplate(img, cross_template, cv2.TM_CCOEFF_NORMED) >= 0.8)
                        
                        if tick_coordinates[0].size > 0:
                            pyautogui.mouseUp()
                            pyautogui.click(x = tick_coordinates[1][0] + 5, y = tick_coordinates[0][0] + 5)
                        
                        elif cross_coordinates[0].size > 0:
                            pyautogui.mouseDown(x = cross_coordinates[1][0] + 35, y = cross_coordinates[0][0] + 65)
                            time.sleep(0.1)
                            pyautogui.moveTo(x = x, y = y)
                        
                        else:
                            return
        
        if x < 5: #if the next loop is the end of this for loop dont scroll
            time.sleep(0.5)
            pyautogui.moveTo(x = 800, y = 300)
            time.sleep(0.2)
            pyautogui.scroll(clicks = -90) #if new building is not found scroll dows the list to check
            time.sleep(2)
    pyautogui.click(x = 1860, y = 500) #clicking on the edge to return to the home screen
    global new_building_flag
    new_building_flag = False

def builder_search_upgrade(): #search upgrade function
    pyautogui.moveTo(x = 800, y = 300)
    time.sleep(0.2)
    pyautogui.scroll(clicks = 500) #scrolling to the top of the upgrade building list
    time.sleep(2)

    for x in range(1, 5): #looping four times to ckeck the list fully
        for building_number in range(building_count):
            img = take_screenshot() #taking a screenshot of the list

            template = cv2.imread('templates\\buildings\\search upgrade buildings\\' + str(building_number + 1) + '.png') #loading the search upgarde building image
            
            coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)

            template = cv2.imread('templates\\suggested upgrades.png') #loading suggested upgrade image
            
            _coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.65)
            
            y = 0
            if _coordinates[0].size > 0: #suggested upgrade image found
                for y in range(coordinates[0].size): #looping through the possible position of the search upgrade building image
                    if coordinates[0][y] > _coordinates[0][0]: #checking wether the search upgrade building image is below the suggested upgrade image or not
                        pyautogui.click(x = coordinates[1][y], y = coordinates[0][y]) #clicking on the search upgrade building image which is below the suggested upgrade image
                        return

            elif coordinates[0].size > 0: #suggested upgrade not found but search upgrade building image found
                pyautogui.click(x = coordinates[1][0], y = coordinates[0][0]) #clicking on the search upgrade building image
                return
        
        if x < 4: #if the next loop is the end of this for loop dont scroll
            time.sleep(0.5)
            pyautogui.moveTo(x = 800, y = 300)
            time.sleep(0.2)
            pyautogui.scroll(clicks = -90) #if search upgrade building is not found scroll dows the list to check
            time.sleep(2)
    
    global search_upgrade_flag
    search_upgrade_flag = False

def builder_suggested_upgrade():
    pyautogui.moveTo(x = 900, y = 300)
    time.sleep(0.2)
    pyautogui.scroll(clicks = 400) #scrolling to top of the upgrade building list
    time.sleep(2)
    
    img = take_screenshot() #taking a screenshot of the upgrade building list
    template = cv2.imread('templates\\suggested upgrades.png') #loading suggested upgrade image
    
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.65)
    if coordinates[0].size > 0: #suggested upgrade image found
        pyautogui.click(x = coordinates[1][0] + 50, y = coordinates[0][0] + 55) #clicking on the building name just below the suggested upgrade image

def upgrade_button():
    img = take_screenshot() #taking a screenshot to find the position of upgrade button
    template = cv2.imread('templates\\upgrade button.png') #loading the upgrade button image
    
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.75)
    if coordinates[0].size > 0: #upgrade button image found
        pyautogui.click(x = coordinates[1][0] + 20, y = coordinates[0][0] + 20) #clicking on the upgrade button
        time.sleep(0.5)
        pyautogui.click(x = 950, y = 810) #clicking on the spend resource button
    time.sleep(0.5)
    pyautogui.click(x = 1860, y = 500) #clicking on the edge to return to the home screen
    time.sleep(0.5)

assign_builder()