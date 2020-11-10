import numpy as np
from itertools import product
import random
from random import sample
import GUI as g

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


# -1 - definitely safe
# 1 - hole
# 4 - may be a hole
# 2 - monster
# 5 - may be a monster
# 3 - coins
# 12 - both dangers
# 8 - agent
def validPos(world, pos):
    return pos[1]>=0 and pos[1] < world_width and pos[0]>=0 and pos[0] < world_height


def times(k, direction):
    return (k*direction[0], k*direction[1])

up = (-1,0)
down = (1,0)
left = (0,-1)
right = (0,1)
class Agent:
    def __init__(self):
        #originally was a standalone class, but this solution seems simpler
        self.kb = np.zeros((world_height, world_width), dtype=np.int8)
        self.visited = np.zeros((world_height, world_width), dtype=np.int8)
        self.wumpus_dead = False

        self.pos = agent_start_pos
        self.arrows = 1
        self.points = 0

        world[self.pos] = '8'
        self.writeDown(self.pos, -1)
        self.visited[self.pos] = 1

    #tell
    def writeDown(self, pos, val):
        self.kb[pos] = val
    
    #ask
    def lookUp(self, pos):
        return self.kb[pos]


    def move(self, delta):
        newPos = (self.pos[0]+delta[0],self.pos[1]+delta[1])
        if not validPos(world, newPos) : return "bump"
        self.points -= 1
        if self.dangersCheck() <= 0:
            world[self.pos] = '0'
            self.pos = newPos
            world[self.pos] = '8'
            self.writeDown(self.pos, -1)
            self.visited[self.pos] += 1
        else:
            return "game over"


    def shouldDig(self):
        return self.lookUp(self.pos) == 3

    def digGold(self):
        if world[self.pos] == 3:
            self.points += 1000
            world[self.pos] = 0
        return


    def shoot(self, target):
        if target == self.pos:
            print("i feel you")
        elif self.arrows > 0:
            self.arrows -= 1
            if world[target] == 2:
                return "scream"
            return "klank"
        else :return "no arrows"
    
    def shootDir(self, dir):
        if self.arrows > 0:
            self.arrows -= 1
            for i in range(world_height):
                target = self.posAfterMove(times(i, dir))
                if world[target] == 2:
                    return "scream"
            return "klank"
        else :return "no arrows"


    def dangersCheck(self):
        if world[self.pos] == 1:
            self.points -= 1000
            return 0
        if world[self.pos] == 2:
            return 1
        return -1


    def getNearPos(self):
        up_pos = (self.pos[0]+up[0], self.pos[1]+up[1])
        down_pos = (self.pos[0]+down[0], self.pos[1]+down[1])
        left_pos = (self.pos[0]+left[0], self.pos[1]+left[1])
        right_pos = (self.pos[0]+right[0],self.pos[1]+right[1])
        vals = list()
        if validPos(world, up_pos):
            vals.append(up_pos)
        if validPos(world, down_pos):
            vals.append(down_pos)
        if validPos(world, left_pos):
            vals.append(left_pos)
        if validPos(world, right_pos):
            vals.append(right_pos)
        return vals


    def getSensorData(self):
        near_pos = self.getNearPos()
        sensor_vals = list()
        for pos in near_pos:
            if world[pos] != 0:
                if world[pos] != 3:
                    sensor_vals.append(world[pos])
        if world[self.pos] == 3:
            sensor_vals.append(3)
        return sensor_vals
        

    def writeSensorData(self, data):
        near_pos = self.getNearPos()
        if len(data) < 1:
            for pos in near_pos:
                self.writeDown(pos, -1)
        
        for d in data:
            if d == 2 and self.wumpus_dead:
                continue
            if d == 3:
                self.writeDown(self.pos, d)
                continue
            for pos in near_pos:
                if self.lookUp(pos) < 0 or self.lookUp(pos) == d+3:
                    continue
                elif self.lookUp(pos) == 0:
                    self.writeDown(pos, d+3)
                    continue
                elif (d+3) not in data:
                    self.writeDown(pos, -1)
                    continue
                else:
                    self.writeDown(pos, 12)
        #make some conclusions if possible
        if len(self.getSafeMoves()) == 0:
            target = random.choice(self.getNearPos())
            if self.shoot(target) == "scream":
                self.wumpus_dead == True
                self.writeDown(target, -1)



    def isSafeMove(self, move):
        new_pos = self.pos[0]+move[0], self.pos[1]+move[1]
        if validPos(world, new_pos):
            if self.lookUp(new_pos) <0 or self.lookUp(new_pos) == 3:
                return True
        return False


    def getSafeMoves(self):
        safe_moves = list()
        if self.isSafeMove(up):
            safe_moves.append(up)
        if self.isSafeMove(down):
            safe_moves.append(down)
        if self.isSafeMove(left):
            safe_moves.append(left)
        if self.isSafeMove(right):
            safe_moves.append(right)
        return safe_moves
    
    def posAfterMove(self, move):
        return (self.pos[0]+move[0], self.pos[1]+move[1])

    def chooseMove(self):
        safe_moves = self.getSafeMoves()
        min_move_val = 1000
        best_move = up
        for move in safe_moves:
            if self.visited[self.posAfterMove(move)] < min_move_val:
                min_move_val = self.visited[self.posAfterMove(move)]
                best_move = move
        return best_move


if __name__ == "__main__":
    dude = Agent()
    dude.writeSensorData(dude.getSensorData())
    print(world) 
    while len(dude.getSafeMoves()) > 0 :
        dude.writeSensorData(dude.getSensorData())
        dude.move(dude.chooseMove())
        dude.writeSensorData(dude.getSensorData())
        g.drawWorld(world, dude.wumpus_dead)
        print(world)
        if dude.shouldDig():
            dude.digGold()
            print(world)
            print(dude.points)
            break

        