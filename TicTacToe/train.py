from tictacToeEnv import TicTacToeEnv
from agent import TicAgent

env = TicTacToeEnv()

Agent1 = TicAgent(1,env.all_states,env)
Agent2 = TicAgent(2,env.all_states,env)


train_duration = int(1e5)


def myprint(state):
    for i in range(3):
        for j in range(3):
            print(" ", state[i][j], end=' ')
        print("\n")


def train_agent():
    global train_duration
    global Agent1
    global Agent2
    global env
    agent1Wincount = 0
    agent2Wincount = 0
    drawcount = 0

    for i in range(0,train_duration):
        if i%10000 == 0:
            print("Epochs: ",i, " completed")
            print("Agent 1 won: ", agent1Wincount)
            print("Agent 2 won: ", agent2Wincount)
            print("Draw count: ", drawcount)
            #print(Agent1.valueestimate)
            #print(Agent2.valueestimate)
        #print("Epoch: ",i)
        state, _, _, _ = env.reset()
        Agent1.reset()
        Agent2.reset()
        Agent1.set_state(state)
        Agent2.set_state(state)
        #print("env reset state")
        #myprint(state)
        turnId = 0
        while True:
            x,y = 0,0
            #print(state)
            if(turnId == 0):
                x, y = Agent1.findaction()
            else:
                x, y = Agent2.findaction()
            action = 3*x + y
            state, reward, done, ret = env.step(action)
            Agent1.set_state(state)
            Agent2.set_state(state)
            turnId = (turnId + 1)%2
            if done:
                if ret == 1:
                    #print("Player 1 won")
                    agent1Wincount = agent1Wincount +1
                elif ret == 2:
                    #print("Player 2 won")
                    agent2Wincount = agent2Wincount + 1
                else:
                    drawcount = drawcount + 1
                    #print("Draw")
                break
        Agent1.backup()
        Agent2.backup()
    Agent1.save_policy()
    Agent2.save_policy()
    print("Agent 1 won: ", agent1Wincount)
    print("Agent 2 won: ", agent2Wincount)
    print("Draw count: ", drawcount)


if __name__ == '__main__':
    train_agent()