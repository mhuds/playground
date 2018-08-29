#!/usr/bin/env python3
import os
import cv2
import pyautogui
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from collections import defaultdict
from random import random
import ClickForCoins as cc
import checkForX as cfx

def takescreencap(picname):
    pyautogui.screenshot(picname)

def find_supplies(cv_picref):
    template = cv2.imread('tools.jpg',0)
    res = cv2.matchTemplate(cv_picref,template,cv2.TM_CCOEFF_NORMED)
    threshold=0.8
    loc=np.where(res>=threshold)
    return loc

def find_zzzs(cv_picref):
    template = cv2.imread('zzz.jpg',0)
    res = cv2.matchTemplate(cv_picref,template,cv2.TM_CCOEFF_NORMED)
    threshold=0.8
    loc=np.where(res>=threshold)
    return loc

def start_bevs(locations):
    template = cv2.imread('beverages.jpg',0)
    w,h = template.shape[::-1]
    w = w/2.0
    h = h/2.0
    cx=-1
    cy=-1
    threshold=0.8
    print(locations)
    for pair in locations:
        if(cx==pair[0] or cy==pair[1]):
            continue
        cx = pair[0]
        cy= pair[1]
        print("Moving to: ",cx,cy)
        pyautogui.moveTo(cx,cy+75,duration=random())
        sleep(random()*2)
        pyautogui.click()
        sleep(2)
        bevscreen="bevshot.jpg"
        if os.path.exists(bevscreen):
            os.remove(bevscreen)
        takescreencap(bevscreen)
        bevgray=cv2.imread(bevscreen,0)
        bevs = cv2.matchTemplate(bevgray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(bevs>=threshold)
        by = loc[0]
        bx = loc[1]
        if len(bx)==0:
            print("No bevs!")
            safe=cfx.x_safety()
            continue
        print("I think produce is here:",(bx[0]+(w/2)),(by[0]+(h/2)))
        pyautogui.moveTo(bx[0]+(w/2),by[0]+(h/2),duration=random())
        sleep(random()*3)
        pyautogui.click()
        sleep(random()*1.5)
        safe = cfx.x_safety()
        
            
def pyg(x1,x2,y1,y2):
    xd=np.abs(x2-x1)
    yd=np.abs(y2-y1)
    return np.sqrt((xd**2)+(yd**2))

def pythagorean_cleanse(locations,limit):
    x = locations[1]
    y = locations[0]
    dups=[]
    idx = list(range(len(x)))
    idx.reverse()
    flow_control = True
    indx=0
    while(flow_control):
        xt=x[indx]
        yt=y[indx]
        for i in range(len(x)):
            if (xt==x[i] and yt==y[i]):
                continue
            if pyg(xt,x[i],yt,y[i])<limit:
                print("Duplicate: ",x[i],y[i])
                dups.append(i)
                continue
        dups.reverse()
        for i in range(len(dups)):
            x=np.delete(x,i)
            y=np.delete(y,i)
        dups=[]
        flow_control=(indx+1<len(x))
        if(flow_control):
            indx = indx+1
    return list(zip(x,y))
            
def get_supplies():
    if os.path.exists("screencap.jpg"):
        os.remove("screencap.jpg")
    picname="screencap.jpg"
    takescreencap(picname)
    cvPic=cv2.imread(picname,0)
    locations=find_supplies(cvPic)
    cleaned_locs=cc.clear_duplicate_locs(locations)
    cc.get_rich(cleaned_locs)
    sleep(5)
    takescreencap(picname)
    cvPic=cv2.imread(picname,0)
    locations=find_zzzs(cvPic)
    cleaned_locs=cc.clear_duplicate_locs(locations)
    start_bevs(cleaned_locs)

if __name__ == "__main__":
    while(True):
        try:
            if os.path.exists("screencap.jpg"):
                os.remove("screencap.jpg")
            picname="screencap.jpg"
            
            takescreencap(picname)
            cvPic=cv2.imread(picname)
            cvPicGray = cv2.cvtColor(cvPic,cv2.COLOR_BGR2GRAY)
            locations = find_supplies(cvPicGray)
            cleaned_locs=cc.clear_duplicate_locs(locations)
            #cleaned_locs=pythagorean_cleanse(locations,50)
            
            '''
            Click on all the 'tools'
            '''
            cc.get_rich(cleaned_locs)
            sleep(5)
            
            '''
            Start up beverage production again
            '''
            takescreencap(picname)
            cvPic=cv2.imread(picname)
            cvPicGray=cv2.cvtColor(cvPic,cv2.COLOR_BGR2GRAY)
            locations = find_zzzs(cvPicGray)
            cleaned_locs=cc.clear_duplicate_locs(locations)
            start_bevs(cleaned_locs)
            
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except OSError:
            print("Screensaver?")
            break