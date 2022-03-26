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
directions = {
    'Right' : [0, 1],
    'Left' : [0, -1],
    'Up' : [-1, 0],
    'Down' : [1, 0]
}
opposite_directions = {
    'Right' : 'Left',
    'Left' : 'Right',
    'Up' : 'Down',
    'Down' : 'Up'
}

class Driver:

    def __init__(self, road_map):

        coordinates = initialise_driver_position(road_map)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.direction = initialise_driver_direction(self.x, self.y, road_map)
        self.next_direction = self.direction
        self.change_direction = False

    def move_forward(self):
        direction = directions[self.direction]
        x_move = direction[0]
        y_move = direction[1]

        new_x = self.x + x_move
        new_y = self.y + y_move

        if road_map[new_x][new_y] != 3:
            self.x = new_x
            self.y = new_y

        if new_x > 0 and new_x < 50 and new_y >0 and new_y < 50:
            if road_map[new_x][new_y] == 3:
                #print("New x is " + str(new_x))
                #print("New y is " + str(new_y))
                #print("Road map at [x, y] is " + str(road_map[new_x][new_y]))
                print(find_junction_direction_options(road_map, new_x, new_y))

        

def initialise():

    global road_map, drivers, locations

    ## Initialising a random road map and lists of drivers and their locations
    road_map = create_random_road_map()
    drivers = []
    locations = []

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
    plt.scatter(drivers_y, drivers_x, color="red")
    plt.show()

def update():
    
    for driver in drivers:
        driver.move_forward()

pycxsimulator.GUI().start(func=[initialise, observe, update])