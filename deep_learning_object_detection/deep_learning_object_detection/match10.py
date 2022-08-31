import numpy as np
import argparse
import imutils
import glob
import matplotlib.pyplot as plt
from PIL import ImageGrab
import cv2
import time
import pyautogui
import keyboard
import os

np.set_printoptions(threshold=10000)

keyboard.add_hotkey('esc', lambda: os._exit(1))


def img_find(template, size):
    template2 = cv2.Canny(template, 50, 200)
    screen = np.array(ImageGrab.grab(bbox=size))
    processed_img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    found = (0, 0, 0, 0)
    n=0
    for scale in np.linspace(0.7, 1.3, 7)[::-1]:
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = float(gray.shape[1]) / float(resized.shape[1])
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template2, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        print (r)
        loc = np.where(result >= threshold)
        #print (loc)
        for pt in zip(*loc[::-1]):
            n=n+1
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if maxVal > found[0]:
            found = (maxVal, (maxLoc[0]*r), (maxLoc[1]*r), r)
        print (found)
    return (found[0], int(found[1]), int(found[2]), processed_img, n, found[3])



def img_proc(template, size):
    start_time = time.time()
    (tH, tW) = template.shape[:2]
    xcoord = 0
    ycoord = 0
    while(True):
        value = img_find(template, size)
        time_elap = time.time() - start_time
        if time_elap >= 5:
            print ("can't find the image 1")
            cv2.imshow("Image", value[3])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            #os._exit(1)
            h=0
            break
        if value[4] > 1:
            print ("there is more than 1 match. To abort, hit escape. If selection is correct, close the screen to continue")
            xcoord = value[1]
            ycoord = value[2]
            cv2.rectangle(value[3], (xcoord, ycoord), (xcoord+int(tW*value[5]), ycoord+int(tH*value[5])), (0, 0, 255), 2)
            cv2.imshow("Image", value[3])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            xcoord = size[0] + value[1] + tW/2
            ycoord = size[1] + value[2] + tH/2
            h=1
            break
        if value[0] >= 0.5:
            xcoord = size[0] + value[1] + tW/2
            ycoord = size[1] + value[2] + tH/2
            h=1
            break
    return (xcoord, ycoord, h)

# pyautogui.moveTo(100, 200)   # moves mouse to X of 100, Y of 200.
# pyautogui.moveTo(None, 500)  # moves mouse to X of 100, Y of 500.
# pyautogui.moveTo(600, None)  # moves mouse to X of 600, Y of 500.
# pyautogui.moveTo(100, 200, 2)   # moves mouse to X of 100, Y of 200 over 2 seconds
# pyautogui.moveTo(100, 200)  # moves mouse to X of 100, Y of 200.

# pyautogui.move(0, 50)       # move the mouse down 50 pixels.
# pyautogui.move(-30, 0)      # move the mouse left 30 pixels.
# pyautogui.move(-30, None)   # move the mouse left 30 pixels.

# pyautogui.dragTo(100, 200, button='left')     # drag mouse to X of 100, Y of 200 while holding down left mouse button
# pyautogui.dragTo(300, 400, 2, button='left')  # drag mouse to X of 300, Y of 400 over 2 seconds while holding down left mouse button
# pyautogui.drag(30, 0, 2, button='right')   # drag the mouse left 30 pixels over 2 seconds while holding down the right mouse button

# pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)     # start slow, end fast
# pyautogui.moveTo(100, 100, 2, pyautogui.easeOutQuad)    # start fast, end slow
# pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad)  # start and end fast, slow in middle
# pyautogui.moveTo(100, 100, 2, pyautogui.easeInBounce)   # bounce at the end
# pyautogui.moveTo(100, 100, 2, pyautogui.easeInElastic)  # rubber band at the end

# pyautogui.click()  # click the mouse

# pyautogui.click(x=100, y=200)  # move to 100, 200, then click the left mouse button.

# pyautogui.click(button='right')  # right-click the mouse

# pyautogui.click(clicks=2)  # double-click the left mouse button
# pyautogui.click(clicks=2, interval=0.25)  # double-click the left mouse button, but with a quarter second pause in between clicks
# pyautogui.click(button='right', clicks=3, interval=0.25)  ## triple-click the right mouse button with a quarter second pause in between clicks

# pyautogui.doubleClick()  # perform a left-button double click

# pyautogui.mouseDown(); pyautogui.mouseUp()  # does the same thing as a left-button mouse click
# pyautogui.mouseDown(button='right')  # press the right button down
# pyautogui.mouseUp(button='right', x=100, y=200)  # move the mouse to 100, 200, then release the right button up.

# pyautogui.scroll(10)   # scroll up 10 "clicks"
# pyautogui.scroll(-10)  # scroll down 10 "clicks"
# pyautogui.scroll(10, x=100, y=100)  # move mouse cursor to 100, 200, then scroll up 10 "clicks"

# pyautogui.hscroll(10)   # scroll right 10 "clicks"
# pyautogui.hscroll(-10)   # scroll left 10 "clicks"

# pyautogui.typewrite('Hello world!')                 # prints out "Hello world!" instantly
# pyautogui.typewrite('Hello world!', interval=0.25)  # prints out "Hello world!" with a quarter second delay after each character

# pyautogui.keyDown('shift')  # hold down the shift key
# pyautogui.press('left')     # press the left arrow key
# pyautogui.press('left')     # press the left arrow key
# pyautogui.press('left')     # press the left arrow key
# pyautogui.keyUp('shift')    # release the shift key

#### ________________________________________________________________


#### example:


# load in your template and tell it where on screen to look
template5 = cv2.imread(r'C:\Users\JJ\Desktop\images\test1.jpg', 0)
size5 = (100, 100, 2000, 1500)

# look for template and return coordinates and pass/fail value)
img2 = img_proc(template5, size5)

# if fail, try something else (in this case, drag an icon somewhere else), and run the match template function again
if img2[2] == 0:
    pyautogui.moveTo (2356, 1230)
    pyautogui.dragTo(350, 350, 1, button='left')
    img2 = img_proc(template5, size5)

# if pass, perform action (in this case, double click)
if img2[2] == 1:
    pyautogui.doubleClick(img2[0], img2[1])


