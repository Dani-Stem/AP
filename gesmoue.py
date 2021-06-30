from datetime import timedelta
import mediapipe
import cv2
import numpy as np
import handTrackMod as htm
import time
import autopy
import pyautogui
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/home/dani/Desktop/apMirror")
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://music.apple.com/")

def playSong(userInput):
    driver.find_element(By.CSS_SELECTOR, ".dt-search-box__input").click()
    driver.find_element(By.CSS_SELECTOR, ".dt-search-box__input").send_keys(userInput)
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, ".dt-search-box__input").send_keys(Keys.ENTER)
    time.sleep(5)
    driver.find_element_by_xpath("//*[@class='shelf-grid__list']/li/div/div/div/div/div/button").click()
    song = driver.find_element_by_xpath("//*[@class='shelf-grid__list']/li/div/div/div/ul/li/span/span").text
    artist = driver.find_element_by_xpath("//*[@class='shelf-grid__list']/li/div/div/div/ul/li[2]/a").text
    return "Playing {0} by {1}".format(song, artist)

time.sleep(10)

playSong("AP by Pop smoke")

def resumeOrPause():
    driver.find_element_by_xpath(
        "//*[@class='web-chrome-playback-controls__directionals']/div[2]/button[2]").click()
    time.sleep(2)
def nextSong():
        driver.find_element_by_xpath(
            "//*[@class='web-chrome-playback-controls__directionals']/div[2]/button[3]").click()
        time.sleep(2)


time.sleep(10)

##########################
wCam, hCam = 640, 460
frameR = 80  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)
click_switch = True
keyboard = Controller()


time0 = 0
delta = 0
while True:
    #Find hand Landmarks
    success, img = cap.read()
    if not success: continue
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    #Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

    #Check which fingers are up
    fingers = detector.fingersUp()

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
    # #Index/second Finger Moving cursor
    # if (fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0):
    #     # 5. Convert Coordinates
    #     x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    #     y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
    #     # 6. Smoothen Values
    #     clocX = plocX + (x3 - plocX) / smoothening
    #     clocY = plocY + (y3 - plocY) / smoothening

    if (fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0):
        resumeOrPause()
        print("yeePP")

    if (fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] ==0):
        nextSong()
        print("yeeNext")

        # #Move Mouse
        # autopy.mouse.move(wScr - clocX, clocY)
        # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        # plocX, plocY = clocX, clocY

    # #clicking w/ index finger & releasing the click w/ first 2 fingers
    # if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
    #     pyautogui.mouseDown(button='left')
    #     pyautogui.mouseUp(button='left')
    #
    # # ScrollING
    # if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
    #     time0 = time.time()x_pos = detector.lmList[1][2]
    #     delta = prev_x_pos - x_pos
    #     if y0 > y1:
    #         pyautogui.scroll(75)
    #         print('up')
    #     if y0 < y1:
    #         pyautogui.scroll(-75)
    #         print('down')
    #
    #     print(time0)
    #     print(y0)
    #     print(y1)
    #
    #     y1 = detector.lmList[1][2]
    #Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    #Display
    cv2.imshow("Image", img)
    cv2.moveWindow("Image", 1800, 0)
    # cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)


