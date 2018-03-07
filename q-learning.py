import numpy as np
np.random.seed(0)

from agent import agent
from Grid import Grid

class QLearning:

    def __init__(self, agent):
        self.grid = agent.grid
        self.agent = agent
        self.nA = agent.nA
        self.size1 = self.grid.size1
        self.Q = np.zeros((self.size1**2,self.nA))
        
    def learn(self,depth=100,exploration_rate=.2, alpha=1, gamma=.95):
        t = 0
        for _ in range(depth):
            
            random_step = np.random.binomial(1,exploration_rate)
            
            best_a = np.argmax(self.Q[self.agent.convert_location_to_state(),:])
            if random_step:
                a = np.random.choice(self.nA)
            else:
                a = best_a
            r = self.get_reward(a)
            best_r = self.get_reward(best_a)
            
            
            new_belief = self.Q[self.agent.convert_location_to_state(),a] + \
                        alpha * (r + gamma * best_r 
                                    - self.Q[self.agent.convert_location_to_state(),a])
            self.Q[self.agent.convert_location_to_state(),a] = new_belief
            self.agent.simulate_step(a)    
    
    def get_reward(self, a):
        return self.agent.get_reward(a) + self.grid.get_reward()[0] 
        
    def choose_action(self):
        return np.argmax(self.Q[self.agent.convert_location_to_state(),:])
        
        
if __name__ == '__main__':
    grid = Grid()
    grid.add_agent()
    grid.add_agent()
    ql = QLearning(grid.agents[0])
    print(ql.choose_action())
    ql.learn()
    print(ql.choose_action())