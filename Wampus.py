import numpy as np
from itertools import product
import random
from random import sample
# import matplotlib

# -- CONFIG --
world_width = 10
world_height = 4
num_holes = 6
num_borders = 3
num_gold = 2
num_monster = 1
# ------------
knowledge_base = {1: "breeze", 2: "bang", 3: "shine", 4: "growl"}
world = np.zeros((world_height, world_width), dtype=np.int8)
events = sample(list(product(range(world_height), range(world_width))), k=num_holes + num_borders + num_gold+num_monster)

holes = events[:num_holes]
borders = events[num_holes:num_holes+num_borders]
gold = events[num_holes+num_borders:num_holes+num_borders+num_gold]
monster = events[num_holes+num_borders+num_gold:]


def place_event(world, locations, number):
    for coord in locations:
        i, j = coord
        world[i, j] = number
    return world


'''
def place_holes(world, number_holes, number):
    holes = 0
    for i in range(world_width):
        if i != 0 and i != world_width-1 and random.choice([True, False]):
            world[4, i] = number
'''

world = place_event(world, holes, 1)
world = place_event(world, borders, 2)
world = place_event(world, gold, 3)
world = place_event(world, monster, 4)


def get_knowledge(world, knowledge_base, pos_i, pos_j):
    location_knowledge = ""
    if pos_i != 0:
        top = world[pos_i-1, pos_j]
        if top:
            location_knowledge = location_knowledge + knowledge_base[top] + "; "
    if pos_i != len(world) - 1:
        bottom = world[pos_i+1, pos_j]
        if bottom:
            location_knowledge = location_knowledge + knowledge_base[bottom] + "; "
    if pos_j != 0:
        left = world[pos_i, pos_j-1]
        if left:
            location_knowledge = location_knowledge + knowledge_base[left] + "; "
    if pos_j != len(world) - 1:
        right = world[pos_i, pos_j+1]
        if right:
            location_knowledge = location_knowledge + knowledge_base[right] + "; "
    if location_knowledge != "":
        print(location_knowledge)
    else:
        print("nothing around")


# 1 - hole
# 2 - wall
# 3 - coins
# 4 - monster
# 8 - agent


if __name__ == "__main__":
    agent_pos_i = 7
    agent_pos_j = 2
    get_knowledge(world, knowledge_base, agent_pos_j, agent_pos_i)
    world[agent_pos_j, agent_pos_i] = '8'
    print(world)
