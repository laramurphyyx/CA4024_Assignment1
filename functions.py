###
### Importing necessary packages
###

import random
import numpy as np
import pandas as pd

junction_paths = {
    ("Left", "Up") : [3, 2, 0],
    ("Left", "Down") : [3],
    ("Right", "Up") : [0],
    ("Right", "Down") : [0, 1, 3],
    ("Up", "Left") : [2],
    ("Up", "Right") : [2, 0, 1],
    ("Down", "Left") : [1, 3, 2],
    ("Down", "Right") : [1],
    }

global map_size
map_size = 50

def set_map_size(set_map_size):
    global map_size
    map_size = set_map_size

def create_random_road_map():

    ###
    ### Creating 2 random coordinates for both horizontal and vertical roads
    ### These roads can't be 5 units from eachother or 5 units from the edge
    ###

    horizontal_roads = []
    vertical_roads = []

    horizontal_roads.append(random.randint(5, map_size-5))
    horizontal_road = random.randint(5, map_size-5)
    while horizontal_road - horizontal_roads[0] in range(-5,5):
        horizontal_road = random.randint(5, map_size-5)
    horizontal_roads.append(horizontal_road)

    vertical_roads.append(random.randint(5, map_size-5))
    vertical_road = random.randint(5, map_size-5)
    while vertical_road - vertical_roads[0] in range(-5,5):
        vertical_road = random.randint(5, map_size-5)
    vertical_roads.append(vertical_road)

    ###
    ### Using matrix to visualise junctions, horizontal roads and vertical roads
    ### - Horizontal roads are represented by a 1
    ### - Vertical roads are represented by a 2
    ### - Junctions are represented by a 3
    ###

    road_map = np.zeros((map_size,map_size))

    for x_coord in horizontal_roads:
        for y_coord in range(0,map_size):
            road_map[x_coord][y_coord] += 1
            road_map[x_coord + 1][y_coord] += 1

    for y_coord in vertical_roads:
        for x_coord in range(0,map_size):
            road_map[x_coord][y_coord] += 2
            road_map[x_coord][y_coord + 1] += 2

    # Adding top and bottom horizontal edge roads
    left_vertical_road = min(vertical_roads)
    right_vertical_road = max(vertical_roads) + 1
    for x_coord in [0, map_size-2]:
        for y_coord in range(0,map_size):
            if y_coord >= left_vertical_road and y_coord <= right_vertical_road:
                road_map[x_coord][y_coord] += 1
                road_map[x_coord + 1][y_coord] += 1

    # Adding left and right vertical edge roads
    top_horizontal_road = min(horizontal_roads)
    bottom_horizontal_road = max(horizontal_roads) + 1
    for y_coord in [0, map_size-2]:
        for x_coord in range(0,map_size):
            if x_coord >= top_horizontal_road and x_coord <= bottom_horizontal_road:
                road_map[x_coord][y_coord] += 2
                road_map[x_coord][y_coord + 1] += 2

    return road_map

def check_coordinates_in_boundaries(x, y):
    if x < 0 or x >= map_size:
        return False
    elif y < 0 or y >= map_size:
        return False
    return True

def initialise_driver_position(road_map):

    ###
    ### Getting the coordinates of all possible positions (horizontal/vertical roads, no junctions) 
    ###

    horizontal_roads = np.array(np.where(road_map==1)).T
    vertical_roads = np.array(np.where(road_map==2)).T

    all_roads = []
    for coordinate in horizontal_roads:
        all_roads.append([coordinate[0], coordinate[1]])
    for coordinate in vertical_roads:
        all_roads.append([coordinate[0], coordinate[1]])

    ###
    ### Assigning initial coordinates
    ###

    coordinates = random.choice(all_roads)
    x = coordinates[0]
    y = coordinates[1]

    return [x, y]

def initialise_driver_direction(x, y, road_map):

    horizontal_roads = np.array(np.where(road_map==1)).T
    horizontal_roads = [coordinate.tolist() for coordinate in horizontal_roads]

    if [x, y] in horizontal_roads:

        # Driver can only be going either left or right
        # Choosing left or right depends on what lane they are in

        if x == 0:
            return "Right"
        elif road_map[x-1][y] == 1:
            return "Left"
        else:
            return "Right"

    else:

        # Driver can only be going either up or down
        # Choosing up or down depends on what lane they are in

        if y == 0:
            return "Up"
        elif road_map[x][y-1] == 2:
            return "Down"
        else:
            return "Up"

    return road_map[x][y]

def find_coordinates_of_junction(road_map, x, y):

    coordinates_of_junction = []

    for x_coord in [x-1, x, x+1]:
            for y_coord in [y-1, y, y+1]:
                if check_coordinates_in_boundaries(x_coord, y_coord):
                    if road_map[x_coord][y_coord] == 3:
                        coordinates_of_junction.append([x_coord, y_coord])

    return coordinates_of_junction

def find_junction_direction_options(road_map, x, y):

    coordinates_of_junction = find_coordinates_of_junction(road_map, x, y)

    # if x = 0 in any of them then 'up' is not an option
    # if x = 49 in any of them then 'down' is not an option
    # if y = 0 in any of them then 'left' is not an option
    # if y = 49 in any of them then 'right' is not an option
    for coordinate in coordinates_of_junction:
        x = coordinate[0]
        y = coordinate[1]

        if x == 0:
            # This is either junction on the top horizontal road
            for y_coord in [y-1, y-2]:
                if road_map[x][y_coord] == 1:
                    return ['Left', 'Down']
                elif road_map[x][y_coord] == 0:
                    return ['Right', 'Down']

        elif x == map_size-1:
            # This is either junction on the bottom horizontal road
            for y_coord in [y-1, y-2]:
                if road_map[x][y_coord] == 1:
                    return ['Left', 'Up']
                elif road_map[x][y_coord] == 0:
                    return ['Right', 'Up']

        elif y == 0:
            # This is either junction on the top vertical road
            for x_coord in [x-1, x-2]:
                if road_map[x_coord][y] == 2:
                    return ['Right', 'Up']
                elif road_map[x_coord][y] == 0:
                    return ['Right', 'Down']

        elif y == map_size-1:
            # This is either junction on the bottom vertical road
            for x_coord in [x-1, x-2]:
                if road_map[x_coord][y] == 2:
                    return ['Left', 'Up']
                elif road_map[x_coord][y] == 0:
                    return ['Left', 'Down']
    else:
        return ['Right', 'Left', 'Up', 'Down']

def input_customised_map_size():

    # Accepting customised map size
    input_map_size = input("Enter a map size (or leave empty to use the default map size of 50):")

    # Ensuring the map size is an integer
    while input_map_size:
        try:
            int(input_map_size)
            # Ensuring the map is not smaller than 15
            if int(input_map_size) < 15:
                input_map_size = input("Map size is too small. Please enter a map size greater than 15 (or leave empty to use the default map size of 50):")
            else:
                break
        except:
            input_map_size = input("Map size must be an integer. Please enter a map size (or leave empty to use the default map size of 50):")

    # Ensuring map size is greater than 15
    while input_map_size and int(input_map_size) < 15:
        input_map_size = input("Map size is too small. Please enter a map size greater than 15 (or leave empty to use the default map size of 50):")

    # Setting map size
    if input_map_size:
        map_size = int(input_map_size)
        set_map_size(map_size)
        return map_size
    else:
        return 50


def input_customised_number_drivers():

    # Accepting customised number of drivers
    input_number_drivers = input("Enter a number of drivers (or leave empty to use the default number of drivers of 10):")

    # Ensuring the number of drivers is an integer
    while input_number_drivers:
        try:
            int(input_number_drivers)
            # Ensuring the number of drivers can physically fit on the map
            maximum_number_drivers = (4 * map_size) - 48
            if int(input_number_drivers) > maximum_number_drivers:
                input_number_drivers = input("Map cannot fit more than " + str(maximum_number_drivers) + " drivers. Please enter a smaller number (or leave empty to use the default number of drivers of 10):")
            else:
                break
        except:
            input_number_drivers = input("Number of drivers must be an integer. Please enter a number of drivers (or leave empty to use the default number of drivers of 10):")

    # Setting map size
    if input_number_drivers:
        return int(input_number_drivers)
    else:
        return 10