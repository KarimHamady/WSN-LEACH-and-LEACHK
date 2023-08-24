import math
WAVE_VELOCITY = 3 * math.pow(10, 8)
from parameters import *

def distance(location1, location2):
    squaredXdiff = math.pow((location1[0] - location2[0]), 2)
    squaredYdiff = math.pow((location1[1] - location2[1]), 2)
    return math.sqrt(squaredXdiff + squaredYdiff)

def propagationDelay(distance, velocity=WAVE_VELOCITY):
    return distance/velocity