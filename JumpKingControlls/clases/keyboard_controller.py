import numpy as np
import cv2 as cv
import win32api
import win32con
import keyboard


class KeyboardController:
    @staticmethod
    def press_key(key):
        keyboard.press(key)

    @staticmethod
    def release_key(key):
        keyboard.release(key)
