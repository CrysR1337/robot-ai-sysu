import numpy as np
import math
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255,0)
blue = (0, 0, 255)
yellow = ( 255,200,0)
purple = (128,138,135)

def get_angle_diff(yaw1, yaw2):
    diff = yaw2 - yaw1
    if diff < -180:
        diff = diff + 360
    elif diff > 180:
        diff = diff - 360
    return diff

def get_yaw(x1, y1, x2, y2):
    return float(int(270 - np.math.atan2(y2-y1, x2-x1) * 180 / 3.1415926)%360)


def get_distance(x1, y1, x2, y2):
    return np.power((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2), 0.5)

def get_action(ain):
    a0 = int(ain / 18)
    action1 = [0, 0, 0, 0]
    if a0 == 0:
        action1[0] = 0
    elif a0 == 1:
        action1[0] = -3
    elif a0 == 2:
        action1[0] = 3
    ain = ain % 18

    a0 = int(ain / 6)
    if a0 == 0:
        action1[1] = 0
    elif a0 == 1:
        action1[1] = -3
    elif a0 == 2:
        action1[1] = 3
    ain = ain % 6

    a0 = int(ain / 2)
    if a0 == 0:
        action1[2] = 0
    elif a0 == 1:
        action1[2] = -3
    elif a0 == 2:
        action1[2] = 3
    ain = ain % 2

    a0 = int(ain % 2)
    if a0 == 0:
        action1[3] = 0
    elif a0 == 1:
        action1[3] = 1
    return action1
