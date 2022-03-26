import pycxsimulator
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from functions import *

###
### Assigning Simulation Variables
###

number_drivers = 10
drivers = []
locations = []

class Driver:

    def __init__(self, road_map):

        coordinates = initialise_driver_position(road_map)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.direction = initialise_driver_direction(self.x, self.y, road_map)

def initialise():

    global road_map

    ## Initialising a random road map
    road_map = create_random_road_map()

    ## Initialising each driver
    for i in range(0, number_drivers):
        driver = Driver(road_map)

        # Ensuring no two drivers start in the same location
        while [driver.x, driver.y] in locations:
            driver = Driver(road_map)

        drivers.append(driver)
        locations.append([driver.x, driver.y])

def observe():

    plt.cla()
    plt.imshow(road_map)
    drivers_x =  [driver.x for driver in drivers]
    drivers_y =  [driver.y for driver in drivers]
    plt.scatter(drivers_y, drivers_x)
    plt.show()

def update():
    pass

initialise()
observe()