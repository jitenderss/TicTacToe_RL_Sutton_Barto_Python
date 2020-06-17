from tictacToeEnv import TicTacToeEnv
from agent import TicAgent
from heuristics import RandomAgent
from heuristics import MinMaxAgent

env = TicTacToeEnv()

def run_rl_agent_only_test(test_duration):
    global env
    agent1 = TicAgent(1, env.all_states, env)
    agent2 = TicAgent(2, env.all_states, env)
    agent1.load_policy()
    agent2.load_policy()
    agent1.training = False
    agent2.training = False

    agent1Wincount = 0
    agent2Wincount = 0
    drawcount = 0

    for i in range(0, test_duration):
        #print("Epoch: ", i)
        state, _, _, _ = env.reset()
        agent1.reset()
        agent2.reset()
        agent1.set_state(state)
        agent2.set_state(state)
        turnId = 0
        while True:
            x, y = 0, 0
            if (turnId == 0):
                x, y = agent1.findaction()
            else:
                x, y = agent2.findaction()
            action = 3 * x + y
            state, reward, done, ret = env.step(action)
            agent1.set_state(state)
            agent2.set_state(state)
            turnId = (turnId + 1) % 2
            if done:
                if ret == 1:
                    #print("Player 1 won")
                    agent1Wincount = agent1Wincount + 1
                elif ret == 2:
                    #print("Player 2 won")
                    agent2Wincount = agent2Wincount + 1
                else:
                    drawcount = drawcount + 1
                    #print("Draw")
                break
    print("Agent 1 won: ", agent1Wincount)
    print("Agent 2 won: ", agent2Wincount)
    print("Draw count: ", drawcount)


def run_test_heuristics_only(test_duration):
    global env
    agent2 = RandomAgent(2,env)
    agent1 = MinMaxAgent(1,env)

    agent1Wincount = 0
    agent2Wincount = 0
    drawcount = 0

    for i in range(0, test_duration):
        #print("Epoch: ", i)
        state, _, _, _ = env.reset()
        agent1.reset()
        agent2.reset()
        turnId = 0
        while True:
            x, y = 0, 0
            #print("turnId: ",turnId)
            if (turnId == 0):
                x, y = agent1.findaction(state)
            else:
                x, y = agent2.findaction(state)
            action = 3 * x + y
            state, reward, done, ret = env.step(action)
            turnId = (turnId + 1) % 2
            if done:
                if ret == 1:
                    #print("Player 1 won")
                    agent1Wincount = agent1Wincount + 1
                elif ret == 2:
                    #print("Player 2 won")
                    agent2Wincount = agent2Wincount + 1
                else:
                    drawcount = drawcount + 1
                    #print("Draw")
                break
    print("Agent 1 won: ", agent1Wincount)
    print("Agent 2 won: ", agent2Wincount)
    print("Draw count: ", drawcount)


def run_rl_agent_heuristic_test(test_duration):
    global env
    agent1 = TicAgent(1, env.all_states, env)
    #agent2 = TicAgent(2, env.all_states, env)
    agent2 = MinMaxAgent(2,env)#RandomAgent(2,env)#MinMaxAgent(2,env)
    agent1.load_policy()
    agent1.training = False
    #agent2.load_policy()

    agent1Wincount = 0
    agent2Wincount = 0
    drawcount = 0

    for i in range(0, test_duration):
        #print("Epoch: ", i)
        state, _, _, _ = env.reset()
        agent1.reset()
        agent2.reset()
        agent1.set_state(state)
        turnId = 0
        while True:
            x, y = 0, 0
            if (turnId == 0):
                x, y = agent1.findaction()
            else:
                x, y = agent2.findaction(state)
            action = 3 * x + y
            state, reward, done, ret = env.step(action)
            agent1.set_state(state)
            turnId = (turnId + 1) % 2
            if done:
                if ret == 1:
                    #print("Player 1 won")
                    agent1Wincount = agent1Wincount + 1
                elif ret == 2:
                    #print("Player 2 won")
                    agent2Wincount = agent2Wincount + 1
                else:
                    drawcount = drawcount + 1
                    #print("Draw")
                break
    print("Agent 1 won: ", agent1Wincount)
    print("Agent 2 won: ", agent2Wincount)
    print("Draw count: ", drawcount)

def run_heuristic_rl_agent_test(test_duration):
    global env
    agent2 = TicAgent(2, env.all_states, env)
    #agent2 = TicAgent(2, env.all_states, env)
    agent1 = MinMaxAgent(1,env)#RandomAgent(2,env)#MinMaxAgent(2,env)
    agent2.load_policy()
    agent2.training = False
    #agent2.load_policy()

    agent1Wincount = 0
    agent2Wincount = 0
    drawcount = 0

    for i in range(0, test_duration):
        #print("Epoch: ", i)
        state, _, _, _ = env.reset()
        agent1.reset()
        agent2.reset()
        agent2.set_state(state)
        turnId = 0
        while True:
            x, y = 0, 0
            if (turnId == 0):
                x, y = agent1.findaction(state)
            else:
                x, y = agent2.findaction()
            action = 3 * x + y
            state, reward, done, ret = env.step(action)
            agent2.set_state(state)
            turnId = (turnId + 1) % 2
            if done:
                if ret == 1:
                    #print("Player 1 won")
                    agent1Wincount = agent1Wincount + 1
                elif ret == 2:
                    #print("Player 2 won")
                    agent2Wincount = agent2Wincount + 1
                else:
                    drawcount = drawcount + 1
                    #print("Draw")
                break
    print("Agent 1 won: ", agent1Wincount)
    print("Agent 2 won: ", agent2Wincount)
    print("Draw count: ", drawcount)



if __name__ == '__main__':
    #run_rl_agent_only_test(int(1e3))          # P1 RL agent P2 RL agent
    #run_test_heuristics_only(int(1e3))
    #run_rl_agent_heuristic_test(int(1e3))     # P1 RL agent P2 MinMax agent
    run_heuristic_rl_agent_test(int(1e3))      # P1 MinMax P2 RL agent