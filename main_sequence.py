#!/usr/bin/env python3

import ClickForCoins as cfc
import ClickForSupplies as cfs
import os
import numpy as np
import cv2
import pyautogui
from time import sleep

if __name__=='__main__':
    while(True):
        try:
            cfc.get_coins()
            sleep(5)
            cfs.get_supplies()
            sleep(300)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except OSError:
            print("Screensaver turn on?")
            break