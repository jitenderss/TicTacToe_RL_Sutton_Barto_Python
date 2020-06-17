import gym
from gym import error, spaces, utils
from gym.utils import seeding

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


class TicTacToeEnv(gym.Env):
    ##### Player 1 have value 1 in TicTacToe grid
    ##### Player 2 have value 2 in TicTacToe grid
    def __init__(self):
        self.state = [[0 for i in range(3)] for j in range(3)]
        self.iter = 0
        self.reward = 0.
        self.done = 0
        self.n = 3
        self.all_states = None
        self.generate_allstates()
        #self.agentid = 0 # RL agent will be first one always as of now

    def mapstates(self,state):
        h = 0
        for i in range(3):
            for j in range(3):
                h = 3*h + state[i][j]
        return h

    def count1and2(self,state):
        count1 = 0
        count2 = 0
        for x in state:
            for y in x:
                if y == 1:
                    count1 = count1 + 1
                elif y == 2:
                    count2 = count2 + 1
        return count1, count2

    def recursivegenerate(self,i,j,init_state):
        if i == self.n and j == self.n:
            cnt1, cnt2 = self.count1and2(init_state)
            if abs(cnt1 - cnt2) > 1:
                return
            if cnt1 < cnt2:
                return
            if cnt1 == cnt2 and self.gameover(init_state) == 1:
                return
            if cnt1 > cnt2 and self.gameover(init_state) == 2:
                return
            newstate = [x[:] for x in init_state]
            hashId = self.mapstates(newstate)
            self.all_states[hashId] = newstate
            return
        init_state[i][j] = 0
        new_j = j + 1
        new_i = i
        if new_j == self.n:
            if new_i != self.n - 1:
                new_j = 0
            new_i = i + 1

        self.recursivegenerate(new_i, new_j, init_state)
        init_state[i][j] = 1
        self.recursivegenerate(new_i, new_j, init_state)
        init_state[i][j] = 2
        self.recursivegenerate(new_i, new_j, init_state)

    def generate_allstates(self):
        #print("generate_allstates")
        self.all_states = dict()
        init_state = [[0 for i in range(3)] for j in range(3)]
        hashId = self.mapstates(init_state)
        #print("hid: ",hashId)
        self.all_states[hashId] = init_state
        self.recursivegenerate(0,0,init_state)
        return self.all_states

    def gameover(self,state):
        for id in range(1,3):
            ##  row check
            for i in range(3):
                res = True
                for j in range(3):
                    if state[i][j] != id:
                        res = False
                        continue
                if res == True:
                    return id

            ##  col check
            for i in range(3):
                res = True
                for j in range(3):
                    if state[j][i] != id:
                        res = False
                        continue
                if res == True:
                    return id

            ## Diag check
            if (state[0][0] == id) and (state[1][1] == id) and (state[2][2] == id):
                return id
            if (state[0][2] == id) and (state[1][1] == id) and (state[2][0] == id):
                return id

        #Check if it's a tie and game is ended
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:   # means game is still going on as there is a 0 remaining
                    return False

        return 3   # 3 is Tie

    def step(self, action):
        if action< 0 or action >8:
            print("Invalid action")
            return self.state,self.reward,self.done

        row = int(action/3)
        col = action%3
        if self.state[row][col] != 0:
            print("Invalid action")
            self.done = 1
            return [self.state, self.reward, self.done,-1]

        self.state = [x[:] for x in self.state]
        #self.state = list(self.state)
        if self.iter%2 == 0:
            self.state[row][col] = 1
            #print("action: ",action, "iter: ",self.iter)
        else:
            self.state[row][col] = 2
            #print("action: ", action, "iter: ", self.iter)

        #myprint(self.state)
        ret = self.gameover(self.state)
        if ret:
            self.done = 1
            #print("Result ", ret)


        self.iter = self.iter + 1
        if self.iter > 8:
            self.done = 1

        return [self.state,self.reward,self.done,ret]

    def reset(self):
        self.state = [[0 for i in range(3)] for j in range(3)]
        self.iter = 0
        self.reward = 0.
        self.done = 0
        return self.state,self.reward,self.done, -1
        #self.agentid = 0
