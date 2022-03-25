import pycxsimulator
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from create_map import *

class driver:
    pass

def initialise():

    global road_map
    road_map = create_random_road_map()

def observe():

    plt.cla()
    plt.imshow(road_map)
    plt.show()

def update():
    pass

initialise()
observe()