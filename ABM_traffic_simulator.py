import pycxsimulator
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from functions import *

###
### Assigning Simulation Variables
###

number_drivers = 10

class driver:

    def __init__(self, road_map):
        coordinates = initialise_driver_position(road_map)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.direction = initialise_driver_direction(self.x, self.y, road_map)

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