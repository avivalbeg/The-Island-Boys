import numpy as np
from Grid import Grid

class Learning:
    def __init__(self,env):
        self.env = env
        self.nA = self.env.nA

    def MCTS(self,env,depth=2):
        N_0 = {}
        Q_0 = {}
        for layer in depth:
            for action in range(self.nA):
                return







class MCTS:
    def __init__(self,env,N0 = None,Q0 = None,T = None):
        self.Tree = []
        if Q0 == None:
            self.Q = np.zeros(env.nS, env.nA)
            self.Q0 = np.zeros(env.nS, env.nA)
        if N0 == None:
            self.N = np.zeros(env.nS,env.nA)
            self.N0 = np.zeros(env.nS, env.nA)
        if T == None:
            self.T = []

        if N0 != None:
            self.N = N0
            self.N0 = np.zeros(env.nS, env.nA)
        if Q0 != None:
            self.Q = Q0
            self.Q0 = np.zeros(env.nS, env.nA)
        if T != None:
            self.T = T

    def select_action(self,s,d,num_episodes = 100):
        self.T = []
        for _ in range(num_episodes):
            self.simulate(s,d)   #the initial policy is considered to be unknown
        return np.argmax(self.Q,axis=1) #Returns the action for each of the agents

    def simulate(self,s,d):
        if d == 0:
            return 0
        if s not in self.T: #checking if the state has already been visited
            for a in range(self.nA):
                self.N[s]


if __name__ == '__main__':
    grid = Grid(n=5)
    grid.add_agent(location=(3, 3))
    grid.add_agent(location=(3, 4))
    done = False
    while not done:
        for agent in grid.agents:
            print(agent.location)
            print(agent.last_action)
        print('-----------')
        actions = input('actions:')
        R,done = grid.time_step(actions=actions)
        Reward = R
        #done = done
        grid.show_grid()
    for agent in grid.agents:
        print(agent.convert_location_to_state())
    print(grid.get_reward())
    print(grid.agents)

