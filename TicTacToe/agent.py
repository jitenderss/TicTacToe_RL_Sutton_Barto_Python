import numpy as np
import operator
import pickle


def myprint(state):
    for i in range(3):
        for j in range(3):
            print(" ", state[i][j], end=' ')
        print("\n")


class TicAgent:
    def __init__(self,id,all_states,env):
        self.playerId = id
        self.epsilon = 0.1
        self.stepsize = 0.1
        self.training = True
        self.states = []
        self.valueestimate = dict()
        self.env = env
        self.initValueEstimates(all_states)

    def initValueEstimates(self,all_states):
        for item in all_states:
            state = all_states[item]
            ret = self.env.gameover(state)
            if ret == False:
                self.valueestimate[item] = 0.5
            else:
                if ret == self.playerId:
                    self.valueestimate[item] = 1.0
                elif ret == 3:  ### Tie
                    self.valueestimate[item] = 0.5
                else:
                    self.valueestimate[item] = 0.0

    def reset(self):
        self.states = []
        self.greedy = []
        #self.initValueEstimates()

    def findaction(self):
        #print("player id: ",self.playerId)
        curr_state = self.states[-1]
        #print("curr state")
        #myprint(curr_state)
        next_states = []
        next_positions = []
        for i in range(self.env.n):
            for j in range(self.env.n):
                if curr_state[i][j] == 0:
                    next_positions.append([i,j])
                    nstate = [x[:] for x in curr_state]
                    #nstate = curr_state.deepcopy()
                    nstate[i][j] = self.playerId
                    #print("nstate")
                    #myprint(nstate)
                    hashId = self.env.mapstates(nstate)
                    #print(hashId)
                    next_states.append(hashId)

        if self.training is True and np.random.rand() < self.epsilon:
            action = next_positions[np.random.randint(len(next_positions))]
            #self.greedy[-1] = False
            return action

        value = []
        for hashid,pos in zip(next_states,next_positions):
            #print(hashid,pos)
            value.append((self.valueestimate[hashid], pos))
        #max(self.valueestimate.items(), key=operator.itemgetter(1))[0]
        np.random.shuffle(value)
        value.sort(key=lambda x: x[0], reverse=True)
        action = value[0][1]
        return action

    def set_state(self,state):
        self.states.append(state)

    def backup(self):
        states = [self.env.mapstates(state) for state in self.states]

        for i in reversed(range(len(states) - 1)):
            state = states[i]
            td_error = self.valueestimate[states[i + 1]] - self.valueestimate[state]
            #if td_error != 0:
            #    print("td_error: ",td_error)
            self.valueestimate[state] += self.stepsize * td_error

    def save_policy(self):
        if self.playerId == 1:
            with open('value_function_rl_policy_%s.obj' % 'first_player', 'wb') as f:
                pickle.dump(self.valueestimate, f)
        else:
            with open('value_function_rl_policy_%s.obj' % 'second_player', 'wb') as f:
                pickle.dump(self.valueestimate, f)

    def load_policy(self):
        if self.playerId == 1:
            with open('value_function_rl_policy_%s.obj' % 'first_player', 'rb') as f:
                self.valueestimate = pickle.load(f)
        else:
            with open('value_function_rl_policy_%s.obj' % 'second_player', 'rb') as f:
                self.valueestimate = pickle.load(f)