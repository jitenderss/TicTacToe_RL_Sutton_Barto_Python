import numpy as np

def myprint(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 1:
                #print(" ", state[i][j], end=' ')
                print(" ", " X", end=' ')
            elif state[i][j] == 2:
                #print(" ", state[i][j], end=' ')
                print(" ", " O", end=' ')
            else:
                print(" ", " -", end=' ')
        print("\n")

class RandomAgent:
    def __init__(self,id,env):
        self.env = env
        self.playerId = id

    def findaction(self,state):
        next_positions = []
        for i in range(self.env.n):
            for j in range(self.env.n):
                if state[i][j] == 0:
                    next_positions.append([i, j])
        action = next_positions[np.random.randint(len(next_positions))]
        return action

    def reset(self):
        pass


class MinMaxAgent:
    WIN_VALUE = 1
    DRAW_VALUE = 0
    LOSS_VALUE = -1

    def __init__(self,id,env):
        self.env = env
        self.cache = {}
        self.playerId = id

    def runmin(self,state):
        #print("runmin: ")
        #myprint(state)
        hashId = self.env.mapstates(state)
        if hashId in self.cache:
            #print("cached: ", self.cache[hashId])
            return self.cache[hashId]

        min_value = self.DRAW_VALUE
        action = -1

        ret = self.env.gameover(state)
        otherId = self.playerId % 2 + 1
        if ret == self.playerId:
            min_value = self.WIN_VALUE
            action = -1
            #print("Game over WIN_VALUE for the below state")
            #myprint(state)
        elif ret == otherId:
            min_value = self.LOSS_VALUE
            action = -1
            #print("Game over LOSS_VALUE for the below state")
            #myprint(state)
        else:
            init_state = state
            for i in range(self.env.n):
                for j in range(self.env.n):
                    if init_state[i][j] == 0:
                        newstate = [x[:] for x in init_state]
                        newstate[i][j] = otherId
                        #print("calling runmax for i,j: ", i, j)
                        res, _ = self.runmax(newstate)
                        if res < min_value or action == -1:
                            min_value = res
                            action = 3*i + j

                            # Shortcut: Can't get better than that, so abort here and return this move
                            if min_value == self.LOSS_VALUE:
                                self.cache[hashId] = (min_value, action)
                                #print("min_value, action (",min_value,action," )")
                                return min_value, action

                        self.cache[hashId] = (min_value, action)
        #print("min_value, action (", min_value, action, " )")
        return min_value, action


    def runmax(self,state):
        #print("runmax: ")
        #myprint(state)
        hashId = self.env.mapstates(state)
        if hashId in self.cache:
            #print("cached: ",self.cache[hashId])
            return self.cache[hashId]

        max_value = self.DRAW_VALUE
        action = -1

        ret = self.env.gameover(state)
        otherId = self.playerId%2 + 1

        if ret == self.playerId:
            max_value = self.WIN_VALUE
            action = -1
            #print("Game over WIN_VALUE for the below state")
            #myprint(state)
        elif ret == otherId:
            max_value = self.LOSS_VALUE
            action = -1
            #print("Game over LOSS_VALUE for the below state")
            #myprint(state)
        else:
            init_state = state
            #print("in state:")
            #myprint(init_state)
            for i in range(self.env.n):
                for j in range(self.env.n):
                    if init_state[i][j] == 0:
                        newstate = [x[:] for x in init_state]
                        newstate[i][j] = self.playerId
                        #print("calling runmin for i,j: ",i,j)
                        res, _ = self.runmin(newstate)
                        if res > max_value or action == -1:
                            #print("entered, res: ",res," max_value: ",max_value," action: ",action)
                            max_value = res
                            action = 3*i + j

                            # Shortcut: Can't get better than that, so abort here and return this move
                            if max_value == self.WIN_VALUE:
                                self.cache[hashId] = (max_value, action)
                                #print("max_value, action (", max_value, action, " )")
                                return max_value, action

                        self.cache[hashId] = (max_value, action)
        #print("max_value, action (", max_value, action, " )")
        return max_value, action

    def findaction(self,state):
        score, action = self.runmax(state)
        row = int(action / 3)
        col = action % 3
        return [row,col]

    def reset(self):
        #self.cache = {}
        pass