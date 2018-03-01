import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix as distance
from agent import agent

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
        reward,done = self.get_reward()
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

if __name__ =='__main__':
    grid = Grid()
    agent1 = agent(grid)
    plt.imshow(agent1.see_map())
    plt.show()
    plt.imshow(grid.agent_map)
    plt.show()