import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix as distance


class Grid:
    """
    Make a plain grid for the bots to play in
    input:
        n: size of square grid(int)
        agents: the set of agents

    """
    def __init__(self,n = 100,Map = None,agents=[]):
        self.size = (n,n)
        self.size1 = n
        self.Map = np.zeros(self.size)
        self.agent_map = np.zeros(self.size)
        self.agents = agents
        self.meeting_point = np.random.randint(1,self.size[0],2)

    def add_agent(self,location=None):
        if location == None:
            self.agents.append(agent(self))
        else:
            try:
                self.agents.append(agent(self,location=location))
            except Exception as e:
                print('Error, loc 1: %s'%e)

    def remove_agent(self,index=None):
        if index == None:

            self.agents.pop()
        else:
            try:
                self.agents.pop(index)
            except Exception as e:

                print('Error, loc 2: %s' %e)

    def time_step(self,actions = 'random'):
        """

        :param actions: a size num_Agents numpy array(or string with no spaces) each with the action for each agent to take.
        :return: returns the total reward for the action taken
        """
        if actions == 'random':
            for agent in self.agents:
                action = np.random.choice(np.arange(agent.nA))
                agent.take_step(action)
        else:
            for i,agent in enumerate(self.agents):
                action = int(actions[i])
                agent.take_step(action)
        reward = self.get_reward()
        # print(reward)
        return reward,done

    def Simulate_time_step(self, actions='random'):
        """

        :param actions: a size num_Agents numpy array each with the action for each agent to take
        :return: returns the total reward for the action taken
        """
        print(actions)
        if actions == 'random':
            for agent in self.agents:
                action = np.random.choice(np.arange(agent.nA))
                agent.take_step(action)
        else:
            for i, agent in enumerate(self.agents):
                action = np.argmax(int(actions[i]))
                agent.take_step(action)
        reward = self.get_reward()
        return reward

    def update_state_grid(self):
        self.agent_map = np.zeros(self.size) #Might change later
        for agent in self.agents:
            y,x = agent.location
            self.agent_map[y,x] = 1

    def show_grid(self):
        self.update_state_grid()
        plt.imshow(self.Map+self.agent_map)
        plt.show()

    def get_reward(self):
        """A function of the agents locations"""
        R = 0   #The closer the agents the higher the reward
        locations = []
        r = []
        done = False
        for agent in self.agents:
            locations.append(np.array(agent.location))
            r.append(agent.get_reward())
        s = np.sum(distance(locations,locations),axis=1)
        r = np.array(r)
        if np.sum(s) == 0:
            done = True
            R = 100 + np.sum(r)
        else:
            R = np.sum(1 / (100*s + 1) + r)
        return R,done






class agent:
    """
    represented by a dot they agents are trying to meet in the center
    """

    def __init__(self,grid,location = None,probabilities = None):
        if location ==None:
            self.location = np.random.randint(1,grid.size[0],2)
        elif(type(location)==tuple and len(location)==2):
            self.location = location
        else:
            print('location is not a tuple... Assigning a random tuple to starting location.')
            self.location = np.random.randint(1, grid.size[0], 2)
        self.knowledge = []
        self.nA = 5   #This could be changed later
        self.R = 0
        self.grid = grid
        self.last_action = None


    def simulate_step(self,action,loc = None, probability = 1):
        if loc ==None:
            loc = np.array(self.location)
        mistake = float(np.random.rand())>probability
        if not mistake:
            if action == 0: # Go up
                loc[0] = loc[0]-1
            if action == 1:
                loc[1] = loc[1]+1
            if action == 2:
                loc[0] = loc[0]+1
            if action == 3:
                loc[1] = loc[1]-1
            if action == 4:
                pass
            if loc[0]<=0:
                loc[0]=0
            if loc[1]<=0:
                loc[1]=0
            if loc[0]>self.grid.size1-1:
                loc[0]=self.grid.size1-1
            if loc[1]>self.grid.size1-1:
                loc[1]=self.grid.size1-1

            return loc
        if mistake:
            #Change later
            action = np.random.sample([0,1,2,3,4])
            loc = self.simulate_step(action)
            return loc

    def get_reward(self,action=None):
        if action == None:
            action = agent.last_action
        if action == 4:
            return -.01
        else:
            return -.03

    def take_step(self,action):
        self.location = self.simulate_step(action)
        self.last_action = action





class Learning:
    def __init__(self,env):
        self.env = env
        self.nA = self.env.nA

    def MCTS(self,env,depth=2):
        N_0 = {}
        Q_0 = {}
        for layer in depth:
            for action in range(self.nA):
                return None







# class MCTS:
#     def __init__(self,env,N0 = None,N0= None,Q0 = None):
#         self.Tree = []
#         if Q0 == None:
#             self.Q0 = np.zeros(env.nS, env.nA)
#         if N0 == None:
#             self.N0 = np.zeros(env.nS,env.nA)
#
#         if N0 != None:
#             self.N0 = N0
#         if Q0 != None:
#             self.Q0 = Q0
#
#     def select_action(self,s,d):
#         return None


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
        R,_ = grid.time_step(actions=actions)
        Reward = R[0]
        done = R[1]
        grid.show_grid()
    for agent in grid.agents:
        print(agent.location)
    print(grid.get_reward())
    print(grid.agents)

