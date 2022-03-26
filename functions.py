###
### Importing necessary packages
###

import random
import numpy as np
import pandas as pd

def create_random_road_map():

    ###
    ### Creating 2 random coordinates for both horizontal and vertical roads
    ### These roads can't be 5 units from eachother or 5 units from the edge
    ###

    horizontal_roads = []
    vertical_roads = []

    horizontal_roads.append(random.randint(5, 45))
    horizontal_road = random.randint(5, 45)
    while horizontal_road - horizontal_roads[0] in range(-5,5):
        horizontal_road = random.randint(5, 45)
    horizontal_roads.append(horizontal_road)

    vertical_roads.append(random.randint(5, 45))
    vertical_road = random.randint(5, 45)
    while vertical_road - vertical_roads[0] in range(-5,5):
        vertical_road = random.randint(5, 45)
    vertical_roads.append(vertical_road)

    ###
    ### Using matrix to visualise junctions, horizontal roads and vertical roads
    ### - Horizontal roads are represented by a 1
    ### - Vertical roads are represented by a 2
    ### - Junctions are represented by a 3
    ###

    road_map = np.zeros((50,50))

    for x_coord in horizontal_roads:
        for y_coord in range(0,50):
            road_map[x_coord][y_coord] += 1
            road_map[x_coord + 1][y_coord] += 1

    for y_coord in vertical_roads:
        for x_coord in range(0,50):
            road_map[x_coord][y_coord] += 2
            road_map[x_coord][y_coord + 1] += 2

    # Adding top and bottom horizontal edge roads
    left_vertical_road = min(vertical_roads)
    right_vertical_road = max(vertical_roads) + 1
    for x_coord in [0, 48]:
        for y_coord in range(0,50):
            if y_coord >= left_vertical_road and y_coord <= right_vertical_road:
                road_map[x_coord][y_coord] += 1
                road_map[x_coord + 1][y_coord] += 1

    # Adding left and right vertical edge roads
    top_horizontal_road = min(horizontal_roads)
    bottom_horizontal_road = max(horizontal_roads) + 1
    for y_coord in [0, 48]:
        for x_coord in range(0,50):
            if x_coord >= top_horizontal_road and x_coord <= bottom_horizontal_road:
                road_map[x_coord][y_coord] += 2
                road_map[x_coord][y_coord + 1] += 2

    ###
    ### Saving the result of this randomised road map to a CSV file
    ###

    return road_map

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

    ###
    ### Re-assigning the position if they begin at a junction
    ###

    if x - 1 > 0 and x + 1 < 50 and y - 1 > 0 and y + 1 < 50:
        while road_map[x-1][y] == 3 or road_map[x+1][y] == 3 or road_map[x][y-1] == 3 or road_map[x][y+1] == 3:
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