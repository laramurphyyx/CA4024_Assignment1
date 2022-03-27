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
        self.change_direction = False

    def move_forward(self):
        direction = directions[self.direction]
        x_move = direction[0]
        y_move = direction[1]

        new_x = self.x + x_move
        new_y = self.y + y_move

        # If the drivers next step is not a junction, move forward
        # if new_x > 0 and new_x < 50 and new_y > 0 and new_y < 50:
        if road_map[self.x][self.y] != 3 and road_map[new_x][new_y] != 3:
            self.x = new_x
            self.y = new_y

        # If the drivers next step is a junction, 
        elif road_map[self.x][self.y] != 3 and road_map[new_x][new_y] == 3:
            # Finding the directions the driver can go (can't turn back on itself)
            possible_directions = find_junction_direction_options(road_map, new_x, new_y)
            possible_directions.remove(opposite_directions[self.direction])
            self.change_direction = random.choice(possible_directions)
            self.x = new_x
            self.y = new_y

        # If the driver is on a junction, figure out its next step
        else:
            self.move_driver_on_junction(road_map)

    def move_driver_on_junction(self, road_map):
        current_direction = self.direction
        new_direction = self.change_direction

        if current_direction == new_direction or new_direction==False:
            self.x += directions[current_direction][0]
            self.y += directions[current_direction][1]

        else:
            coordinates_of_junction = sorted(find_coordinates_of_junction(road_map, self.x, self.y))
            required_path = junction_paths[(current_direction, new_direction)]
            current_location = coordinates_of_junction.index([self.x, self.y])

            # If they're exiting the junction or its only one step
            if current_location == required_path[-1]:
                self.x += directions[self.change_direction][0]
                self.y += directions[self.change_direction][1]
                self.direction = new_direction
                self.change_direction = False

            else:
                for step in range(0, len(required_path) - 1):
                    if current_location == required_path[step]:
                        self.x = coordinates_of_junction[required_path[step + 1]][0]
                        self.y = coordinates_of_junction[required_path[step + 1]][1]

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