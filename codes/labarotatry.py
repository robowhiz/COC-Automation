import cv2
import time
import pyautogui
import easyocr
import numpy as np
from PIL import ImageGrab

reader = easyocr.Reader(['en'],gpu = True) #loading easy ocr reader

global var
var = [1, 1, 0, 0, 0, 0, 0, 0, 0]
max_number_of_troops = 45
troop = 11, 23, 0 #suggested troop order

def take_screenshot():
    time.sleep(0.5)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def do_research():
    img = take_screenshot()

    while True:
        template = cv2.imread('templates\\laboratory\\lab' + str(var[0]) + '.png') #loading lab image
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.7)
        if coordinates[0].size > 0:
            pyautogui.click(x = coordinates[1][0] + 20, y = coordinates[0][0] + 20) #clicking on lab
            time.sleep(0.5)
            pyautogui.click(x = 1065, y = 900) #clicking on research button
            break
        
        else:
            var[0] += 1 #incrementing the lab level if the current level lab is not found
            var[1] = 1 #reseting the upgrade troop number if there is any change in lab level
            var[2] = 0
    
    if var[1] > max_number_of_troops:
        var[4] = 0

    if lab_availability() == 1 and var[1] <= max_number_of_troops: #if lab is available and there are troops that are need to be upgraded
        if troop[var[2]] != 0: #checking for suggested troop order
            lab_search_upgrade() #if there is any do search upgrade function
        else: #if there is no order found to orderwise
            lab_orderwise_upgrade()
    
    time.sleep(0.5)
    pyautogui.click(x = 1860, y = 500, interval = 0.5, clicks = 2) #clicking at the edge of the screen two times

def lab_search_upgrade():
    lab_scroll(int((troop[var[2]] - 1)/10)) #scrolling to the required screen

    while True:
        for z in range(0, 2): #looping 2 times for to make sure 14 and 16 are excluded
            if troop[var[2]] == 14 or troop[var[2]] == 16:
                var[2] += 1
        
        if troop[var[2]] == 0: #if troop array is 0 exit
            lab_orderwise_upgrade()
            return
        
        img = take_screenshot()
        template = cv2.imread('templates\\laboratory\\' + str(troop[var[2]]) + '.png') #loading suggested troop image
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.95)
        if coordinates[0].size > 0: #suggested troop found
            img = take_screenshot() #taking screenshot to check for availability of resource
            
            if lab_enough_resource(img, coordinates) == 1: #checking for enough resource and found there is enough resources
                pyautogui.click(x = coordinates[1][0] + 50, y = coordinates[0][0] + 55) #clicking in the troop icon
                time.sleep(0.2)

                img = take_screenshot() #taking screenshot to set lab timer
                set_lab_timer(img) #seting lab timer
                
                time.sleep(0.2)
                pyautogui.click(x = 1355, y = 865) #clicking on the spend button to start the troop upgrade
                
                if var[7] == 1: #after upgrading starts set the not enough resource for suggested upgrade to 0 if it is setted to 1
                    var[7] = 0
                    var[2] = var[8] #reset the suggested troop number
                
                var[4] = 0 #setting lab availability to 0 upon successfull starting of upgrading of troops

                return #if the troop start to upgrade end this function
            
            else: #there is no enough resources
                if var[7] == 0: #checking not enough resource for suggested upgrade is in 0 or not
                    var[8] = var[2] #saving the suggested troop number
                    var[7] = 1
                var[2] += 1 #incrementing to start searching the next troop
                lab_scroll(int((troop[var[2]] - 1)/10) - int((troop[var[2] - 1] - 1)/10)) #if scrolling is necessary scroll
        
        else: #suggested troop not found
            var[2] += 1 #incrementing to start searching the next troop
            lab_scroll(int((troop[var[2]] - 1)/10) - int((troop[var[2] - 1] - 1)/10)) #if scrolling is necessary scroll

def lab_orderwise_upgrade():
    lab_scroll(int((var[1] - 1)/10)) #scroll to the troop position to select the troop

    while True:
        if var[1] == 14 or var[1] == 16: #make sure 14th and 16th troop is excluded
            var[1] += 1

        img = take_screenshot() #taking screenshot to find the troop
        template = cv2.imread('templates\\laboratory\\' + str(var[1]) + '.png') #loading the troop image
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.95)
        if coordinates[0].size > 0: #upgrade troop found
            img = take_screenshot() #taking screenshot to check for availability of resource
            
            if lab_enough_resource(img, coordinates) == 1: #enough resource available
                pyautogui.click(x = coordinates[1][0] + 50, y = coordinates[0][0] + 55) #clicking in the troop icon
                time.sleep(0.2)

                img = take_screenshot() #taking screenshot to set lab timer
                set_lab_timer(img) #seting lab timer
                
                time.sleep(0.2)
                pyautogui.click(x = 1355, y = 865) #clicking on the spend button to start the troop upgrade
                
                if var[5] == 1: #after upgrading starts reset the not enough resource flag
                    var[5] = 0
                    var[1] = var[6] #reset the upgrade troop number
                
                var[4] = 0 #setting lab availability to 0 upon successfull starting of upgrading of troops

                return #if the troop start to upgrade end this function
                
            else: #enough resource not available
                if var[5] == 0:
                    var[6] = var[1] #saving the upgrade troop number
                    var[5] = 1
                var[1] += 1 #incrementing to try to upgrade the next troop
                lab_scroll(int((var[1] - 1)/10) - int((var[1] - 2)/10)) #if scrolling is necessary scroll

        else: #if upgrade troop not found go for next tropp
            var[1] += 1 #incrementing to try to upgrade the next troop
            lab_scroll(int((var[1] - 1)/10) - int((var[1] - 2)/10)) #if scrolling is necessary scroll
        
        if var[1] > max_number_of_troops: #if there is no troop to upgrade terminate the function
            return

def lab_enough_resource(img, coordinates): #checking for enough resource or not
    cropped_img = img[coordinates[0][0] + 120:coordinates[0][0] + 130, coordinates[1][0] - 20:coordinates[1][0] + 30]
    for y in range(3,  8):
        for x in range(0, 50):
            if cropped_img[y][x][0] == 127 and cropped_img[y][x][1] == 136 and cropped_img[y][x][2] == 255:
                return 0
    return 1

def lab_availability(): #to check wether the lab is available for upgrading the troop or not
    time.sleep(1)
    img = take_screenshot()
    template = cv2.imread('templates\\laboratory\\choose what to upgrade.png')
    
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)
    if coordinates[0].size > 0:
        var[4] = 1
        return 1 #lab available
    
    else:
        var[4] = 0
        return 0 #lab not available

def lab_scroll(x):
    if x >= 0:
        for y in range(0, x):
            pyautogui.moveTo(x = 1335, y = 715)
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.moveTo(x = 445, y = 715, duration = 2)
            time.sleep(0.6)
            pyautogui.mouseUp()
    
    else:
        for y in range(x, 0):
            pyautogui.moveTo(x = 485, y = 715)
            pyautogui.mouseDown()
            time.sleep(0.2)
            pyautogui.moveTo(x = 1375, y = 715, duration = 2)
            time.sleep(0.6)
            pyautogui.mouseUp()

def set_lab_timer(img): #function to set the lab timer
    cropped_img = img[747:793, 1200:1360] #crop the image to the upgrade time
    black = np.zeros((cropped_img.shape[0], cropped_img.shape[1], 3), np.uint8) #create a black image of same size as croped image

    for i in range(0, cropped_img.shape[0]): #extract the number image part
        for j in range(0, cropped_img.shape[1]):
            if int(cropped_img[i][j][0]) + int(cropped_img[i][j][1]) + int(cropped_img[i][j][2]) > 762:
                black[i][j] = (0, 0, 255)

    black = cv2.resize(black, (2 * black.shape[1], 2 * black.shape[0])) #doubling the size of the black image
    time.sleep(1)
    upgrade_time = reader.readtext(black, allowlist = "1234567890dHhMm", detail = 0)[0] #extract only the numbers and letter h and d

    if upgrade_time.find("d") != -1 and upgrade_time.find("d") + 1 == len(upgrade_time): #extracting the days if it has only days
        days = int(upgrade_time[0:len(upgrade_time) - 1])
        hours = 0

    elif upgrade_time.find("d") == -1: #extracting the hours if it only hs hours
        hours = int(upgrade_time[0:len(upgrade_time) - 1])
        days = 0
    
    else: #extracting both days and hours if it has both days and hours
        days = int(upgrade_time[0:upgrade_time.find("d")])
        hours = int(upgrade_time[upgrade_time.find("d") + 1:len(upgrade_time) - 1])
    
    var[3] = int(time.time()) + (days * 86400) + (hours * 3600) + 900

while True:
    file = open("datas\\ids\\id.txt", "r")
    content = file.readlines()
    file.close()
    for x in range(0, 9):
        var[x] = int(content[x])
    
    current_time = int(time.time())
    if var[3] <= current_time: #if timer is 0 do research
        var[4] = 1
    
    if var[4] == 1:
        current_program_number = 5
        do_research()
    
    txt = ""
    for x in range(0, 9):
        txt += str(var[x]) + "\n"

    file = open("datas\\ids\\id.txt", "w")
    file.write(txt)
    file.close()
    time.sleep(60)