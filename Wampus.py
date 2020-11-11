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
agent_start_pos = (0, 0)
# ------------
knowledge_base = {1: "breeze", 2: "bang", 3: "shine", 4: "growl"}
world = np.zeros((world_height, world_width), dtype=np.int8)

events = []
number_of_events = num_holes + num_gold + num_monster
for i in range(number_of_events):
    x = random.randint(0, world_height - 1)
    y = random.randint(0, world_height - 1)
    if x == 0:
        y = random.randint(1, world_height - 1)
    while (x,y) in events:
        x = random.randint(0, world_height - 1)
        y = random.randint(0, world_height - 1)
        if x == 0:
            y = random.randint(1, world_height - 1)
    
    events.append((x, y))

holes = events[:num_holes]
gold = events[num_holes:num_holes + num_gold]
monster = events[num_holes + num_gold:]


def place_event(world, locations, number):
    for coord in locations:
        world[coord] = number
    return world


world = place_event(world, holes, 1)
world = place_event(world, gold, 3)
world = place_event(world, monster, 2)

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
# 6 - dead monster
# 7 - can't be a monster
# 3 - gold
# 12 - both dangers
# 8 - agent
def validPos(world, pos):
    return 0 <= pos[1] < world_width and 0 <= pos[0] < world_height


def times(k, direction):
    return k * direction[0], k * direction[1]


up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
class Agent:
    def __init__(self):
        # originally was a standalone class, but this solution seems simpler
        self.kb = np.zeros((world_height, world_width), dtype=np.int8)
        self.visited = np.zeros((world_height, world_width), dtype=np.int8)
        self.wumpus_dead = False

        self.pos = agent_start_pos
        self.arrows = 1
        self.points = 0

        self.writeDown(self.pos, -1)
        self.visited[self.pos] = 1

    # tell
    def writeDown(self, pos, val):
        self.kb[pos] = val

    # ask
    def lookUp(self, pos):
        return self.kb[pos]

    def move(self, delta):
        newPos = (self.pos[0] + delta[0], self.pos[1] + delta[1])
        if not validPos(world, newPos): return "bump"
        self.points -= 1
        if self.dangersCheck() <= 0:
            self.pos = newPos
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
        print("shooting target", target)
        if target == self.pos:
            print("i feel you")
        elif self.arrows > 0:
            self.points -= 1
            self.arrows -= 1
            if world[target] == 2:
                world[target] = 6
                return "scream"
            return "klank"
        else:
            return "no arrows"

    def shootDir(self, diretction):
        print("shooting direction", diretction)
        if self.arrows > 0:
            self.arrows -= 1
            for i in range(world_height):
                target = self.posAfterMove(times(i, diretction))
                if world[target] == 2:
                    world[target] = 6
                    return "scream"
            return "klank"
        else:
            return "no arrows"

    def dangersCheck(self):
        if world[self.pos] == 1:
            self.points -= 1000
            return 0
        if world[self.pos] == 2:
            return 1
        return -1

    def getNearPos(self):
        up_pos = (self.pos[0] + up[0], self.pos[1] + up[1])
        down_pos = (self.pos[0] + down[0], self.pos[1] + down[1])
        left_pos = (self.pos[0] + left[0], self.pos[1] + left[1])
        right_pos = (self.pos[0] + right[0], self.pos[1] + right[1])
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
        if world[self.pos] == 3 or world[self.pos] == 6:
            sensor_vals.append(world[self.pos])
        return sensor_vals

    def writeSensorData(self, data):
        near_pos = self.getNearPos()
        if (2 not in data or 6 in data) and 1 not in data:
            for pos in near_pos:
                self.writeDown(pos, -1)

        for d in data:
            if d == 2 and self.wumpus_dead:
                continue
            if d == 3:
                self.writeDown(self.pos, d)
                continue
            for pos in near_pos:
                if self.lookUp(pos) < 0 or self.lookUp(pos) == d + 3:
                    continue
                elif d == 2 and self.lookUp(pos) == 7 and 1 not in data:
                    self.writeDown(pos, -1)
                    continue
                elif d == 1 and 2 not in data:
                    if self.lookUp(pos) == 2:
                        self.writeDown(pos, -1)
                elif d==2 and 1 not in data:
                    if self.lookUp(pos) == 1:
                        self.writeDown(pos, -1)
                elif self.lookUp(pos) == 0:
                    self.writeDown(pos, d + 3)
                    continue
                
        # make some conclusions if possible
        all_visited_twice = True
        for move in self.getSafeMoves():
            if self.visited[self.posAfterMove(move)]<2:
                all_visited_twice = False
        if 2 in data and all_visited_twice:
            dir = random.choice(self.getUnsafeMoves())
            sensor = self.shootDir(dir)
            if sensor == "scream":
                self.wumpus_dead == True
                for i in range(world_width-1):
                    self.writeDown(self.posAfterMove(times(i,dir)), 7)


    def isSafeMove(self, move):
        new_pos = self.pos[0] + move[0], self.pos[1] + move[1]
        if validPos(world, new_pos):
            if self.lookUp(new_pos) < 0 or self.lookUp(new_pos) == 3:
                return True
        return False

    def getUnsafeMoves(self):
        res = list()
        if not self.isSafeMove(up) and validPos(world, self.posAfterMove(up)):
            res.append(up)
        if not self.isSafeMove(down) and validPos(world, self.posAfterMove(down)):
            res.append(down)
        if not self.isSafeMove(left) and validPos(world, self.posAfterMove(left)):
            res.append(left)
        if not self.isSafeMove(right) and validPos(world, self.posAfterMove(right)):
            res.append(right)
        return res

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
        return self.pos[0] + move[0], self.pos[1] + move[1]

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

    print(world)
    g.drawWorld(world, dude)
    g.pygame.time.delay(500)

    dude.writeSensorData(dude.getSensorData())

    if len(dude.getSafeMoves()) == 0:
        g.pygame.time.delay(250)
        g.drawNoWay()
    while len(dude.getSafeMoves()) > 0:
        dude.writeSensorData(dude.getSensorData())
        if dude.move(dude.chooseMove()) == "game over":
            g.drawGameOver()
            break
        dude.writeSensorData(dude.getSensorData())
        g.drawWorld(world, dude)
        g.pygame.time.delay(250)
        print(world)
        if dude.points < -32 and not dude.wumpus_dead:
            g.drawNoWay()
            break
        if dude.points < -64:
            g.drawNoWay()
            break
        if dude.shouldDig():
            dude.digGold()
            print(world)
            print(dude.points)
            g.pygame.time.delay(250)
            g.drawWinner()
            break
    
