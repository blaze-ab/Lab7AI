import numpy as np
from itertools import product
import random
from random import sample

# -- CONFIG --
world_width = 4
world_height = 4
num_holes = 2
num_borders = 2
num_gold = 1
num_monster = 1
agent_start_pos = (0,0)
# ------------
perceptions = {1: "breeze", 2: "bang", 3: "shine", 4: "growl"}
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
        return location_knowledge
    else:
        return "nothing around"


# 1 - hole
# 2 - wall
# 3 - coins
# 4 - monster
# 8 - agent

class KB:
    def __init__(self):
        self.worldRep = np.zeros((world_height, world_width), dtype=np.int8)

    def tell(self, pos, obj):
        self.worldRep[pos] = obj
    
    def ask(self, pos):
        return self.worldRep[pos]


up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)


class Agent:
    def __init__(self):
        self.kb = KB()
        self.pos = agent_start_pos
        world[self.pos] = '8'

    def move(self, delta):
        newPos = (self.pos[0]+delta[0], self.pos[1]+delta[1])
        if newPos[0] < 0 or newPos[0] >= world_height: return
        if newPos[1] < 0 or newPos[1] >= world_width: return

        world[self.pos] = '0'
        self.pos = newPos
        world[self.pos] = '8'


if __name__ == "__main__":
    dude = Agent()
    print(world, "\n")
    while True:
        dude.move(down)
        print(world, "\n")
        break

