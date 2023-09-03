import cv2
import time
import pyautogui
import easyocr
import numpy as np
from PIL import ImageGrab

reader = easyocr.Reader(['en'],gpu = True) #loading easy ocr reader

def take_screenshot():
    time.sleep(0.5)
    img_raw = ImageGrab.grab()
    img = np.array(img_raw)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

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

    do_attack()