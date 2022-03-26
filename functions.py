###
### Importing necessary packages
###

import random
import numpy as np
import pandas as pd

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

def find_coordinates_of_junction(road_map, x, y):

    coordinates_of_junction = []

    for x_coord in [x-1, x, x+1]:
        if x_coord > 0 and x_coord < 50:
            for y_coord in [y-1, y, y+1]:
                if y_coord > 0 and y_coord < 50:
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
            print("x is " + str(x))
            for y_coord in [y-1, y-2]:
                print("y_coord is " + str(y_coord))
                print("road_map[x][y_coord] is " + str(road_map[x][y_coord]))
                if road_map[x][y_coord] == 1:
                    return ['Left', 'Down']
                elif road_map[x][y_coord] == 0:
                    return ['Right', 'Down']

        elif x == 49:
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

        elif y == 49:
            # This is either junction on the bottom vertical road
            for x_coord in [x-1, x-2]:
                if road_map[x_coord][y] == 2:
                    return ['Left', 'Up']
                elif road_map[x_coord][y] == 0:
                    return ['Left', 'Down']
    else:
        return ['Right', 'Left', 'Up', 'Down']

def move_driver_on_junction2(Driver, road_map):
    current_direction = Driver.direction
    new_direction = Driver.change_direction

    if current_direction == new_direction:
        self.x += directions[current_direction][0]
        self.y += directions[current_direction][1]

    else:

        coordinates_of_junction = sorted(find_coordinates_of_junction(road_map, Driver.x, Driver.y))
        required_path = junction_paths[(current_direction, new_direction)]
        current_location = coordinates_of_junction.index([self.x, self.y])

        # If they just have to turn one step
        if len(required_path) == 1:
            self.x += directions[new_direction][0]
            self.y += directions[new_direction][1]
            self.direction = new_direction
            self.change_direction = False

        for step in range(0, len(required_path) - 1):
            if current_location == required_path[step]:
                x_movement = required_path[step + 1][0] - required_path[step][0]
                y_movement = required_path[step + 1][1] - required_path[step][1]
                self.x += x_movement
                self.y += y_movement
