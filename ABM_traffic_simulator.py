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
crashes = []
all_crashes = []
asleep = []
steps = 0
tiredness_scores = {}
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
left_of_directions = {
    'Right' : 'Up',
    'Left' : 'Down',
    'Up' : 'Left',
    'Down' : 'Right'
}

class Driver:

    def __init__(self, road_map):
        coordinates = initialise_driver_position(road_map)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.direction = initialise_driver_direction(self.x, self.y, road_map)
        self.change_direction = False
        self.tiredness = random.uniform(0, 0.5)
        self.time_asleep = 0
        self.time_of_crash = None

    def move_forward(self):
        direction = directions[self.direction]
        x_move = direction[0]
        y_move = direction[1]

        new_x = self.x + x_move
        new_y = self.y + y_move

        left_car_position_x = new_x + x_move + directions[left_of_directions[self.direction]][0]
        left_car_position_y = new_y + y_move + directions[left_of_directions[self.direction]][1]

        # If the car has already crashed, it can't move
        if [self.x, self.y] in crashes or (road_map[self.x][self.y] == 0):
            if [self.x, self.y] in asleep:
                asleep.remove([self.x, self.y])
            self.x = 0
            self.y = 0
            if not self.time_of_crash:
                self.time_of_crash = steps

        # If the driver is asleep, see if they will wake up
        elif random.uniform(100, 500) < self.time_asleep:
            self.tiredness = 0
            asleep.remove([self.x, self.y])
            self.time_asleep = 0

        # If the driver falls asleep
        elif self.tiredness >= 1:
            if [self.x, self.y] not in asleep:
                asleep.append([self.x, self.y])
                print("Driver has fallen asleep at " + str([self.x, self.y]))
            self.time_asleep += 1

        # If there is a car in front, don't go
        elif [new_x, new_y] in locations:
            if road_map[self.x][self.y] != 3:
                if random.random() < self.tiredness:
                    self.x = new_x
                    self.y = new_y
            self.tiredness += random.uniform(0, 0.2)

        # If there is a car enterring from the left of the junction, don't go
        elif check_coordinates_in_boundaries(new_x, new_y) and [left_car_position_x, left_car_position_y] in locations and road_map[new_x][new_y] == 3:
            if road_map[self.x][self.y] != 3:
                if random.random() < self.tiredness:
                    possible_directions = find_junction_direction_options(road_map, new_x, new_y)
                    possible_directions.remove(opposite_directions[self.direction])
                    self.change_direction = random.choice(possible_directions)
                    self.x = new_x
                    self.y = new_y
            self.tiredness += random.uniform(0, 0.2)

        # If the drivers next step is not a junction, move forward
        # if new_x > 0 and new_x < 50 and new_y > 0 and new_y < 50:
        elif road_map[self.x][self.y] != 3 and road_map[new_x][new_y] != 3:
            self.x = new_x
            self.y = new_y

        # If the drivers next step is a junction, but theyre not on it yet
        elif road_map[self.x][self.y] != 3 and road_map[new_x][new_y] == 3:

            # If there is already someone in the junction, don't go
            coordinates_of_junction = find_coordinates_of_junction(road_map, new_x, new_y)
            junction_in_use = False
            for coordinate in coordinates_of_junction:
                if coordinate in locations:
                    junction_in_use = True

            if junction_in_use and random.random() > self.tiredness:
                self.tiredness += random.uniform(0, 0.2)

            else:
                # Finding the directions the driver can go (can't turn back on itself)
                possible_directions = find_junction_direction_options(road_map, new_x, new_y)
                possible_directions.remove(opposite_directions[self.direction])
                self.change_direction = random.choice(possible_directions)
                self.x = new_x
                self.y = new_y
                self.tiredness += random.uniform(0, 0.01)

        # If the driver is on a junction, figure out its next step
        else:
            self.move_driver_on_junction(road_map)

    def move_driver_on_junction(self, road_map):
        current_direction = self.direction
        new_direction = self.change_direction

        if current_direction == new_direction or new_direction==False:
            self.x += directions[current_direction][0]
            self.y += directions[current_direction][1]
            self.tiredness += random.uniform(0, 0.01)

        else:
            coordinates_of_junction = sorted(find_coordinates_of_junction(road_map, self.x, self.y))
            required_path = junction_paths[(current_direction, new_direction)]
            current_location = coordinates_of_junction.index([self.x, self.y])

            # If they're exiting the junction or its only one step
            if current_location == required_path[-1]:
                self.x += directions[self.change_direction][0]
                self.y += directions[self.change_direction][1]
                self.tiredness += random.uniform(0, 0.01)
                self.direction = new_direction
                self.change_direction = False

            else:
                for step in range(0, len(required_path) - 1):
                    if current_location == required_path[step]:
                        self.x = coordinates_of_junction[required_path[step + 1]][0]
                        self.y = coordinates_of_junction[required_path[step + 1]][1]
                        self.tiredness += random.uniform(0, 0.01)
                        self.direction = new_direction

def initialise():

    global road_map, drivers, locations, steps

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

    steps += 1

def observe():

    ## Plotting the tiredness scores

    plt.subplot(2, 1, 2)
    plt.cla()

    plt.plot([0, steps], [1, 1], '--', color="red", linewidth=0.5)
    for i in range(0, number_drivers):
        driver = drivers[i]
        if i in tiredness_scores:
            tiredness_scores[i].append(driver.tiredness)
        else:
            tiredness_scores[i] = [driver.tiredness]
    for i in range(0, number_drivers):
        if drivers[i].time_of_crash:
            time_of_crash = drivers[i].time_of_crash
            plt.plot(list(np.arange(0, time_of_crash)), tiredness_scores[i][:time_of_crash])
            plt.plot(drivers[i].time_of_crash, drivers[i].tiredness, marker="*", color="orange", markersize=20)
        else:
            plt.plot(list(np.arange(0, steps)), tiredness_scores[i])
    plt.title("Tiredness Scores for Each Driver")
    plt.xlabel("Time (in steps)")
    plt.ylabel("Tiredness Scores")
    plt.ylim([-0.05, 1.15])
        
    ## Plotting the simulation

    plt.subplot(2, 1, 1)
    plt.cla()
    plt.imshow(road_map)

    drivers_x = []
    drivers_y = []
    number_cars_crashed = 0
    for location in locations:
        if location != [0,0]:
            drivers_x.append(location[0])
            drivers_y.append(location[1])
        else:
            number_cars_crashed += 1
    plt.scatter(drivers_y, drivers_x, marker="s", color="red")
    for crash in crashes:
        plt.plot(crash[1], crash[0], marker="*", color="orange", markersize=25)
    plt.text(map_size + 1, map_size - (map_size/10), "Cars crashed: " + str(number_cars_crashed))
    plt.text(map_size + 1, map_size, "Drivers asleep: " + str(len(asleep)))

    plt.tight_layout()

def update():

    global locations, crashes, asleep, steps
    
    for driver in drivers:
        driver.move_forward()

    locations = []
    for driver in drivers:
        locations.append([driver.x, driver.y])

    unique_locations = []
    crashes = []
    for location in locations:
        if location != [0,0]:
            if location in unique_locations:
                crashes.append(location)
            else:
                unique_locations.append(location)

    for crash in crashes:
        print("Crash at " + str(crash))

    steps += 1

map_size = input_customised_map_size()
number_drivers = input_customised_number_drivers()

pycxsimulator.GUI().start(func=[initialise, observe, update])