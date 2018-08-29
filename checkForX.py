#!/usr/bin/env python3
import os
import cv2
import pyautogui
import numpy as np
from time import sleep
from collections import defaultdict
from random import random

def screengrab(picname):
    pyautogui.screenshot(picname)

def find_X(cv_picref,template):
    res=cv2.matchTemplate(cv_picref,template,cv2.TM_CCOEFF_NORMED)
    threshold=0.8
    loc = np.where(res>=threshold)
    return loc

def click_x(coords):
    pyautogui.moveTo(coords[0],coords[1], duration=random())
    sleep(random()*2)
    pyautogui.click()
    print("Clicked X at ",coords[0],coords[1])
    sleep(random()*5)

def x_safety():
    if os.path.exists("xgrap.jpg"):
        os.remove("xgrab.jpg")
    safepic="xgrab.jpg"
    screengrab(safepic)
    cvPicGray=cv2.imread(safepic,0)
    template=cv2.imread('bigX.jpg',0)
    w,h=template.shape[::-1]
    locations=find_X(cvPicGray,template)
    y=locations[0]
    x=locations[1]
    if len(x)==0:
        print("NO X")
        return 0
    w=w/2.0
    h=h/2.0
    coords=[x[0]+w,y[0]+h]
    click_x(coords)
    return 1

if __name__=="__main__":
    if os.path.exists("xgrab.jpg"):
        os.remove("xgrab.jpg")
    picname="xgrab.jpg"
    screengrab(picname)
    cvPic=cv2.imread(picname)
    cvPicGray=cv2.cvtColor(cvPic,cv2.COLOR_BGR2GRAY)
    template = cv2.imread('bigX.jpg',0)
    w,h=template.shape[::-1]
    locations = find_X(cvPicGray,template)
    y=locations[0]
    x=locations[1]
    w = w/2.0
    h = h/2.0
    coords=[x[0]+w,y[0]+h]
    click_x(coords)
