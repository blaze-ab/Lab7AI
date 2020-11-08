import numpy as np
from itertools import product
import random
from random import sample

# -- CONFIG --
world_width = 4
world_height = 4
num_holes = 2
num_gold = 1
num_monster = 1
agent_start_pos = (0,0)
# ------------
knowledge_base = {1: "breeze", 2: "bang", 3: "shine", 4: "growl"}
world = np.zeros((world_height, world_width), dtype=np.int8)
events = sample(list(product(range(world_height), range(world_width))), k=num_holes + num_gold+num_monster)

holes = events[:num_holes]
borders = events[num_holes:num_holes]
gold = events[num_holes:num_holes+num_gold]
monster = events[num_holes+num_gold:]

def place_event(world, locations, number):
    for coord in locations:
        i, j = coord
        world[i, j] = number
    return world

world = place_event(world, holes, 1)
world = place_event(world, monster, 2)
world = place_event(world, gold, 3)


'''def get_knowledge(world, knowledge_base, pos_i, pos_j):
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
        return (location_knowledge)
    else:
        return ("nothing around")'''

def validPos(world, pos):
    return pos[1]>=0 and pos[1] < world_width and pos[0]>=0 and pos[0] < world_height

# -1 - definitely safe
# 1 - hole
# 4 - may be a hole
# 2 - monster
# 5 - may be a monster
# 3 - coins
# 8 - agent
class KB:
    def __init__(self):
        self.worldRep = np.zeros((world_height, world_width), dtype=np.int8)

    def tell(self, pos, val):
        self.worldRep[pos] = val
    
    def ask(self, pos):
        return self.worldRep[pos]


up = (-1,0)
down = (1,0)
left = (0,-1)
right = (0,1)
class Agent:
    def __init__(self):
        self.kb = KB()
        self.pos = agent_start_pos
        self.arrows = 1
        world[self.pos] = '8'
        self.kb.tell(self.pos, -1)

    def move(self, delta):
        newPos = (self.pos[0]+delta[0],self.pos[1]+delta[1])
        if not validPos(world, newPos) : return "bump"

        world[self.pos] = '0'
        self.pos = newPos
        world[self.pos] = '8'
        if self.stillAlive(world):
            self.kb.tell(self.pos, -1)
        else:
            print("game over") 

    def stillAlive(self, ):
        if world[self.pos] == 1 or world[self.pos] == 2:
            return False
        return True

    def getNearPos(self):
        up_pos = (self.pos[0]+up[0], self.pos[1]+up[1])
        down_pos = (self.pos[0]+down[0], self.pos[1]+down[1])
        left_pos = (self.pos[0]+left[0], self.pos[1]+left[1])
        right_pos = (self.pos[0]+right[0],self.pos[1]+right[1])
        vals = list()
        if validPos(world, up_pos):
            vals.append(world[up_pos])
        if validPos(world, down_pos):
            vals.append(world[down_pos])
        if validPos(world, left_pos):
            vals.append(world[left_pos])
        if validPos(world, right_pos):
            vals.append(world[right_pos])
        return vals


    def getSensorData(self):
        near_pos = self.getNearPos()
        sensor_vals = list()
        for pos in near_pos:
            if world[pos] != 0:
                sensor_vals.append(world[pos])
        return sensor_vals
        

    def writeSensorData(self, data):
        near_pos = self.getNearPos()
        for d in data:
            for pos in near_pos:
                if self.kb.ask(pos) == 0:
                    self.kb.tell(pos, d+3)
                elif self.kb.ask(pos) == -1 or self.kb.ask(pos) == d+3:
                    continue
                #elif self.kb.ask(pos) == 3:??????


if __name__ == "__main__":
    dude = Agent()
    print(world)
    while True:
        print(dude.sensor())
        dude.move(down)
        print(world)
        print(dude.sensor())
        break

