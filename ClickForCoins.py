#!/usr/bin/env python3
import os
import cv2
import pyautogui
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from collections import defaultdict
from random import random
import checkForX as cfx

def takescreencap(picname):
    pyautogui.screenshot(picname)

def find_coins(cv_picref):
    template=cv2.imread('coin.jpg',0)
    res=cv2.matchTemplate(cv_picref,template,cv2.TM_CCOEFF_NORMED)
    threshold=0.8
    loc=np.where(res>=threshold)
    return loc

def list_duplicates(sequence):
    '''
    Returns a tuple of each duplicated item, along with the indices in the sequence where
    that item appears
    example:  [12,13,14,14,15,14,15,16] will return a generator that can be output as:
    (14, [2,3,5])
    (15, [4,6])
    
    '''
    tally=defaultdict(list)
    for i, item in enumerate(sequence):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)

def clear_duplicate_locs(locations): #locations should be a tuple of numpy ndarrays
    '''
    The duplicates aren't TRUE duplicates, but they're typically points that share the same
    X coordinate, and have Y coordinates that are off by one.
    #locations[0] -> down (Y)
    #locations[1] -> across (X)
    '''
    x = locations[1]
    y = locations[0]
    for dup in sorted(list_duplicates(x)):
        print("Duplicates: ",dup)
        temp=dup[1]
        temp.reverse() #if you're going to remove elements by index, start from the back
        for idx in range(len(temp)):
            if idx==0:
                continue #keep the first one.  Throw out the rest
            np.delete(x,temp[idx],0)
            np.delete(y,temp[idx],0)
    pairs = zip(x,y)
    return list(pairs)

def get_rich(list_of_locations):
    cx=-1
    cy=-1
    for pair in list_of_locations:
        if(cx==pair[0] or cy==pair[1]):
            continue
        cx=pair[0]
        cy=pair[1]
        pyautogui.moveTo(cx,cy+75,duration=random())
        print("Moving to: ",pair[0],pair[1]+75)
        sleep(random()*2)
        pyautogui.click()
        sleep(random()*5)
        if(cfx.x_safety()>0):
            print("dup missed, dialog handled")

def get_coins():
    if os.path.exists("screencap.jpg"):
        os.remove("screencap.jpg")
    picname="screencap.jpg"
    takescreencap(picname)
    cvPic=cv2.imread(picname,0)
    locations=find_coins(cvPic)
    cleaned_locs = clear_duplicate_locs(locations)
    get_rich(cleaned_locs)

if __name__ == "__main__":
    while(True):
        try:
            if os.path.exists("screencap.jpg"):
                os.remove("screencap.jpg")
            picname="screencap.jpg"
            
            takescreencap(picname)
            #grab picture, make a 'gray' copy
            cvPic = cv2.imread(picname)
            cvPicGray=cv2.cvtColor(cvPic,cv2.COLOR_BGR2GRAY)
            
            locations = find_coins(cvPicGray)
            cleaned_locs = clear_duplicate_locs(locations)
            
            get_rich(cleaned_locs)
            
            sleep(300)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except OSError:
            print("There was a problem.  Did the screensaver start?")
            break
