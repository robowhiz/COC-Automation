import cv2, numpy as np, pyautogui, time, os, easyocr, threading, sys
from PIL import ImageGrab
from flask import Flask, request, send_file, Response, render_template

reader = easyocr.Reader(['en'], gpu = True) #loading easy ocr reader

program_status = True
current_program_number = 0 #returns what is happening in code
current_program = ["opening clash of clans",
                   "waiting for home page",
                   "collecting resources",
                   "removing obstacles",
                   "assingning builders",
                   "starting research",
                   "attacking multiplayer base : 1",
                   "attacking multiplayer base : 2",
                   "traning army",
                   "closing clash of clans",
                   "waiting for next loop"]

recording = True
time_out = False

loop_timer = 0
th = 5
loop_delay = [1, 2, 3, 4, 4, 5, 5]
select_hours = 0
id_number = 1

global var
var = [1, 1, 0, 0, 0, 0, 0, 0, 0]

building_count = 0
search_upgrade_flag = True
new_building_flag = True

max_number_of_troops = 45
troop = 11, 23, 0 #suggested troop order

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

def do_attack():
    pyautogui.click(x = 100, y = 980) #clicking on the attack button
    time.sleep(1)
    pyautogui.click(x = 1380, y = 670) #clicking on the find match button
    
    attack_start_stop(0)
    start_attack()
    attack_start_stop(1)
    
    pyautogui.click(x = 950, y = 890) #clicking on the return home button
    time.sleep(3)
    pyautogui.click(x = 1860, y = 500, clicks = 2, interval = 0.5) #clicking on the edge of the screen to come back to home screen

def attack_start_stop(select):
    if select == 0:
        template = cv2.imread("templates\\attack\\next.png")
        time.sleep(5)
    else:
        time.sleep(20)
        template = cv2.imread("templates\\attack\\return home.png")

    while True:
        img = take_screenshot()
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.9)
        if coordinates[0].size > 0:
            return
        
        time.sleep(1)

def ad_coordinates(img):
    AD_coordinates = [[0,0], [0,0], [0,0], [0,0]]
    AD_levels = [0, 0, 0, 0]
    z = [0, 0]

    def distance(x, y):
        return int(((x[0] - y[0])** 2 + (x[1] - y[1])** 2) ** 0.5)

    for x in range(1, 14):
        template = cv2.imread("templates\\attack\\AD" + str(x) + ".png")

        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.8)
        if coordinates[0].size > 0:
            if z[1] != 0:
                z[1] += 1
            AD_coordinates[z[1]] = [coordinates[1][0], coordinates[0][0]]
            AD_levels[z[1]] = x

            for y in range(1, coordinates[0].size):
                if distance([coordinates[1][z[0]], coordinates[0][z[0]]], [coordinates[1][y], coordinates[0][y]]) > 8 and (coordinates[0][y] - coordinates[0][z[0]] >= 3 or coordinates[1][y] - coordinates[1][z[0]] >= 0):
                    z[1] += 1
                    AD_coordinates[z[1]] = [coordinates[1][y], coordinates[0][y]]
                    AD_levels[z[1]] = x
                    z[0] = y
            
        z[0] = 0

        if AD_coordinates[3][0] != 0:
            return AD_coordinates , AD_levels
    
    return AD_coordinates , AD_levels

def army_count(img, select):
    if select == 0:
        template = cv2.imread("templates\\attack\\lightning spell.png")
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.9)
        if coordinates[0].size > 0:
            cropped_img = img[coordinates[0][0] - 8:coordinates[0][0] + 32, coordinates[1][0] + 72:coordinates[1][0] + 100]
        else:
            return 0
    else:
        template = cv2.imread("templates\\attack\\x.png")
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.9)
        cropped_img = img[921:948, coordinates[1][0] + 20:coordinates[1][0] + 60]

    black = np.zeros((cropped_img.shape[0], cropped_img.shape[1], 3), np.uint8)
    
    for i in range(0, cropped_img.shape[0]): #extract the number image part
        for j in range(0, cropped_img.shape[1]):
            if int(cropped_img[i][j][0]) + int(cropped_img[i][j][1]) + int(cropped_img[i][j][2]) > 762:
                black[i][j] = (0, 0, 255)

    black = cv2.resize(black, (2 * black.shape[1], 2 * black.shape[0])) #doubling the size of the black image
    
    count = reader.readtext(black, allowlist = "1234567890", detail = 0)
    if len(count) > 0:
        return int(count[0])
    else:
        return 0

def _spell_level(img):
    template = cv2.imread("templates\\attack\\lightning spell.png")

    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.9)
    if coordinates[0].size == 0:
        return 0
    cropped_img = img[coordinates[0][0] + 102:coordinates[0][0] + 130, coordinates[1][0]:coordinates[1][0] + 30]
    black = np.zeros((cropped_img.shape[0], cropped_img.shape[1], 3), np.uint8)
    
    for i in range(0, cropped_img.shape[0]): #extract the number image part
        for j in range(0, cropped_img.shape[1]):
            if int(cropped_img[i][j][0]) + int(cropped_img[i][j][1]) + int(cropped_img[i][j][2]) > 720:
                black[i][j] = (0, 0, 255)
    black = cv2.resize(black, (4 * black.shape[1], 4 * black.shape[0])) #doubling the size of the black image
    count = reader.readtext(black, allowlist = "1234567890", detail = 0)
    if len(count) > 0:
        return int(count[0])
    else:
        return 1

def drop_spells(AD_coordinates, AD_levels):
    point1 = np.array([[774,2], [181,454], [1737,448], [1143,2]])
    point2 = np.array([[181,454], [782,902], [1131,902], [1737,448]])
    sum = [0, 0, 0, 0]
    dis = [0, 0, 0, 0]
    side = 0
    total_spells = 0
    
    def perpendicular_distance(p1 , p2 , p3):
        return int(abs(np.cross(p2 - p1, p3 - p1)/np.linalg.norm(p2 - p1)))

    for x in range(0, 4):
        for y in range(0, 4):
            if AD_coordinates[y][0] != 0:
                sum[x] += perpendicular_distance(point1[x], point2[x], AD_coordinates[y])
            else:
                sum[x] += 0

    min = np.sort(sum)[0]

    for i in range(0, 4):
        if min == sum[i]:
            side = i

    for x in range(0, 4):
        if AD_coordinates[x][0] != 0:
            dis[x] = perpendicular_distance(point1[side], point2[side], AD_coordinates[x])
        else:
            dis[x] = 0
    
    dis_sortted = np.sort(dis)
    
    img = take_screenshot()
    
    total_spells = army_count(img, 0)
    spell_level = _spell_level(img)

    def perpendicular_intersection(line_points, external_point):
        x1, y1 = line_points[0]
        x2, y2 = line_points[1]
        p, q = external_point

        a = y1 - y2
        b = x2 - x1
        c = (x1 * y2) - (x2 * y1)

        x = -((a*p) + (b*q) + c)*a
        x /= ((a*a) + (b*b))
        x += p

        y = -((a*p) + (b*q) + c)*b
        y /= ((a*a) + (b*b))
        y += q

        return x, y

    mid_x, mid_y, AD_count = 0, 0, 0
    for x in range(0, 4):
        if AD_coordinates[x][0] != 0:
            AD_count += 1
            foot = perpendicular_intersection([point1[side], point2[side]], AD_coordinates[x])
            mid_x += foot[0]
            mid_y += foot[1]
        else: 
            break
    
    if AD_count != 0:
        mid_x /= AD_count
        mid_y /= AD_count

    mid_point = np.array([mid_x,mid_y])

    if total_spells == 0:
        return side, mid_point
    
    AD_hitpoints = [800, 850, 900, 950, 1000, 1050, 1100, 1210, 1300, 1400, 1500, 1650, 1750]
    spell_damage = [150, 180, 210, 240, 270, 320, 400, 480, 560, 600]

    template = cv2.imread("templates\\attack\\lightning spell.png")
    coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.85)
    if coordinates[0].size > 0:
        pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])
    else:
        return side, mid_point

    if AD_coordinates[0][0] == 0:
        pyautogui.click(x = 920, y = 380, clicks = total_spells, interval = 0.5)
        return side, mid_point
        
    time.sleep(0.5)

    for x in range(0, 4):
        for y in range(0, 4):
            if dis_sortted[x] == dis[y] and AD_coordinates[y][0] != 0:
                required_no_of_spells = int(AD_hitpoints[AD_levels[y] - 1]/spell_damage[spell_level - 1]) + 1
                
                if total_spells < required_no_of_spells:
                    for z in range(0, total_spells):
                        pyautogui.click(x = AD_coordinates[y][0], y = AD_coordinates[y][1])
                        time.sleep(0.5)
                    return side, mid_point
                
                else:
                    for z in range(0, required_no_of_spells):
                        pyautogui.click(x = AD_coordinates[y][0], y = AD_coordinates[y][1])
                        time.sleep(0.5)
                    total_spells -= required_no_of_spells
    
    if total_spells > 0:
        for z in range(0, total_spells):
            pyautogui.click(x = AD_coordinates[1][0], y = AD_coordinates[0][0])
            time.sleep(0.5)
        return side, mid_point
    return side, mid_point

def drop_troops(side, mid_point):
    point1 = np.array([[774,2], [181,454], [1737,448], [1143,2]])
    point2 = np.array([[181,454], [782,902], [1131,902], [1737,448]])

    if mid_point[0] == 0:
        mid_point[0] = (point1[side][0] + point2[side][0])/2
        mid_point[1] = (point1[side][1] + point2[side][1])/2
    
    img = take_screenshot()

    duration = army_count(img, 1)/15

    slope = (point2[side][1] - point1[side][1])/(point2[side][0] - point1[side][0])
    distance = 140

    dx = distance*(1/(1 + (slope*slope)))**0.5
    dy = slope*dx

    pyautogui.click(x = 330, y = 1000)
    for x in range(0, 2):
        pyautogui.moveTo(x = mid_point[0] + dx, y = min(mid_point[1] + dy, 902))
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.moveTo(x = mid_point[0] - dx, y = min(mid_point[1] - dy, 902), duration = duration)
        pyautogui.mouseUp()
        img = take_screenshot()
        if img[930][330][0] == 68 and img[930][330][1] == 68 and img[930][330][2] == 68:
            break
    
    duration = 2.5

    pyautogui.click(x = 455, y = 1000)

    distance = 270
    dx = distance*(1/(1 + (slope*slope)))**0.5
    dy = slope*dx
    pyautogui.moveTo(x = mid_point[0] + dx, y = min(mid_point[1] + dy, 902))
    time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(x = mid_point[0] - dx, y = min(mid_point[1] - dy, 902), duration = duration)
    pyautogui.mouseUp()
    time.sleep(0.5)

def drop_heros_and_seige(img, side):
    point1 = np.array([[774,2], [181,454], [1737,448], [1143,2]])
    point2 = np.array([[181,454], [782,902], [1131,902], [1737,448]])

    for x in range(1, 6):
        template = cv2.imread("templates\\attack\\HS" + str(x) + ".png")

        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.9)
        if coordinates[0].size > 0:
            pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])
            time.sleep(0.5)
            pyautogui.click(x = (point1[side][0] + point2[side][0])/2, y = (point1[side][1] + point2[side][1])/2)
            time.sleep(0.5)
        
    time.sleep(3)
    if coordinates[0].size > 0:
        pyautogui.click(x = coordinates[1][0], y = coordinates[0][0])

def start_attack():
    img = take_screenshot()
    
    AD_datas = ad_coordinates(img)
    AD_coordinates = np.array(AD_datas[0])
    AD_levels = np.array(AD_datas[1])

    side, mid_point = drop_spells(AD_coordinates, AD_levels)
    drop_troops(side, mid_point)

    drop_heros_and_seige(img, side)

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

def set_loop_timer():
    img = take_screenshot()
    global th, loop_delay, select_hours, loop_timer
    for x in range(th, 12):
        template = cv2.imread("templates\\town halls\\th" + str(x) + ".png")
        
        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) >= 0.8)
        if coordinates[0].size > 0:
            break
    
    loop_timer = int(time.time()) + (3600 * loop_delay[select_hours])

def open_clashofclans():
    os.startfile('"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe"')
    time.sleep(30)
    os.system('"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe" --instance Pie64 --cmd launchApp --package com.supercell.clashofclans')
    time.sleep(50)

def close_clashofclans():
    pyautogui.hotkey("ctrl", "left")
    time.sleep(1)
    pyautogui.click(x = 1100, y = 640)
    time.sleep(1)
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    pyautogui.click(x = 1100, y = 590)

def switch_id(position):
    pyautogui.click(x = 1850, y = 830)
    time.sleep(2)
    pyautogui.click(x = 1220, y = 235)
    time.sleep(2)
    pyautogui.click(x = 1700, y = 532 + (102 * position))
    time.sleep(20)

def screen_recording():
    for file in os.listdir("datas\\videos"):
        os.remove(f"datas\\videos\\{file}")

    record_number = 1
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv2.VideoWriter(f"datas\\videos\\output {record_number}.mp4", codec, 10, (1920, 1080))

    time_out_timer = start_time = time.time()
    time_out_timer += 450
    global time_out
    
    while recording:
        img = ImageGrab.grab()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x, y = pyautogui.position()
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
        output.write(img)
        if time.time() - start_time > 120:
            start_time = time.time()
            output.release()
            record_number += 1
            codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            output = cv2.VideoWriter(f"datas\\videos\\output {record_number}.mp4", codec, 10, (1920, 1080))
        
        if time_out_timer < time.time():
            time_out = True
    output.release()

def web_server():
    app = Flask(__name__)

    def html(body):
        html = \
    "<!DOCTYPE html>\n\
    <html>\n\
        <head>\n\
            <title>contents</title>\n\
        </head>\n\
        <body>\n\
            " + body + "\n\
        </body>\n\
    </html>\n"
        return html

    @app.route('/status')
    def get_status():
        global program_status
        return str(program_status)

    @app.route('/timeout')
    def time_out():
        global time_out
        return str(time_out)

    @app.route('/currentprogram')
    def get_current_program():
        global current_program, current_program_number
        return current_program[current_program_number]

    @app.route('/stop')
    def stop_program():
        global program_status
        program_status = False
        return "Program will stop at the next loop"

    @app.route('/start')
    def start_program():
        global program_status
        program_status = True
        return "Program will start at the next loop"

    @app.route('/restart')
    def restart():
        os.system(f"taskkill /PID {os.getpid()} /F & {sys.executable} \"{sys.argv[0]}\"")
    
    @app.route('/closebluestack')
    def closebluestack():
        pyautogui.hotkey("alt", "f4")
        time.sleep(1)
        pyautogui.click(x=1100, y=590)
        return "bluestack closed"
    
    @app.route('/stopall')
    def stop_all():
        pyautogui.hotkey("alt", "f4")
        time.sleep(1)
        pyautogui.click(x=1100, y=590)
        os._exit(1)
    
    @app.route('/')
    def stream():
        return render_template('web server/index.html')
    
    @app.route('/video_feed')
    def video_feed():
        def generate_frames():
            next = 0
            while True:
                if time.time() > next:
                    next = time.time() + 0.1
                    frame = ImageGrab.grab()
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    x, y = pyautogui.position()
                    cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                    frame = cv2.resize(frame, (960, 540))
                    ret = True
                    ret, buffer = cv2.imencode('.jpg', frame)

                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  
    
    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files['file']
        file.save(file.filename)
        return f"{file.filename} upoladed"
    
    @app.route('/click')
    def click():
        x = int(request.args.get('x')) * 2
        y = int(request.args.get('y')) * 2
        pyautogui.click(x = x, y = y)
        return '', 200

    @app.route('/file')
    def file():
        body = ""
        for dir_content in os.listdir():
                body += f"<a href=\"file/{dir_content}\">{dir_content}</a><br>\n"
        return html(body)

    @app.route('/file/<path:link>')
    def display_content(link):
        body = ""
        if  link.find(".ico") > 0:
            return open("templates\\web server\\favicon.ico", "rb")
        
        elif link.find(".mp4") > 0 or link.find(".png") > 0 or link.find(".css") > 0:
            return send_file(link, as_attachment=True)
        
        elif link.find('.') > 0:
            return open(link.replace('/', '\\')).read(), {"Content-Type": "text/plain"}
        
        else:
            path = link.replace('/', '\\')
            for dir_content in os.listdir(path):
                body += f"<a href=\"{link[link.rfind('/') + 1:]}/{dir_content}\">{dir_content}</a><br>\n"

        return html(body)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)

def gaming():
    web_server_thread = threading.Thread(target = web_server)
    web_server_thread.start()
    time.sleep(5)
    global loop_timer, recording, program_status, current_program_number, id_number
    try:
        while True:
            current_time = int(time.time())
            if loop_timer <= current_time and program_status:
                recording = True
                screen_recording_thread = threading.Thread(target = screen_recording)
                screen_recording_thread.start()

                current_program_number = 0
                open_clashofclans()

                def no_of_ids():
                    lst = os.listdir("datas\\ids") #opening the directory of the search upgrade buiding template pictures
                    return len(lst) #counting the number of files in that directory

                def reset_variables():
                    global building_count, search_upgrade_flag, new_building_flag
                    building_count = 0
                    search_upgrade_flag = True
                    new_building_flag = True

                for id_number in range(1, no_of_ids() + 1):
                    file = open("datas\\ids\\id" + str(id_number) + ".txt", "r")
                    content = file.readlines()
                    file.close()
                    for x in range(0, 9):
                        var[x] = int(content[x])

                    reset_variables()

                    current_program_number = 1
                    template = cv2.imread("templates\\trophy.png")
                    while True:
                        img = take_screenshot()

                        coordinates = np.where(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) > 0.85)
                        pyautogui.click(x = 100, y = 970)
                        time.sleep(0.5)
                        pyautogui.click(x = 1860, y = 500)
                        if coordinates[0].size > 0:
                            break
                        time.sleep(2)
                    time.sleep(2)
                    
                    pyautogui.click(x = 980, y = 840)
                    time.sleep(1)
                    pyautogui.click(x = 1860, y = 500)

                    if id_number == 1:
                        set_loop_timer()

                    current_program_number = 2
                    collect_Rewards()
                    collect_resources(1, 5)

                    if builder_availability() == 1:
                        current_program_number = 3
                        remove_obstacles()
                    
                    current_program_number = 4
                    assign_builder()

                    current_time = int(time.time())
                    if var[3] <= current_time: #if timer is 0 do research
                        var[4] = 1
                    
                    if var[4] == 1:
                        current_program_number = 5
                        do_research()
                    
                    current_program_number = 6
                    train_rest()
                    do_attack()
                    time.sleep(5)
                    current_program_number = 7
                    do_attack()
                    time.sleep(2)
                    current_program_number = 8
                    train_army()
                    
                    txt = ""
                    for x in range(0, 9):
                        txt += str(var[x]) + "\n"

                    file = open("datas\\ids\\id" + str(id_number) + ".txt", "w")
                    file.write(txt)
                    file.close()

                    time.sleep(5)

                    if id_number == no_of_ids():
                        switch_id(0)
                    else:
                        switch_id(id_number)

                current_program_number = 9
                close_clashofclans()
                
                time.sleep(5)
                current_program_number =  10
                recording = False

            time.sleep(60)

    except Exception:
        program_status = False

        txt = ""
        for x in range(0, 9):
            txt += str(var[x]) + "\n"
        
        file = open("datas\\ids\\id" + str(id_number) + ".txt", "w")
        file.write(txt)
        file.close()
        
        import traceback
        
        file = open("datas\\error logs.txt", "a")
        date_time = time.ctime()

        logs = "\n" + date_time + "\n"
        logs += traceback.format_exc()

        file.write(logs)
        file.close()

        time.sleep(5)

        recording = False

gaming()