import numpy as np


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

    def convert_location_to_state(self):
        n = self.grid.size1
        s = (n-1)*self.location[0]+self.location[1]
        return s


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
            action = self.last_action
        if action == 4:
            return -.01
        else:
            return -.03

    def take_step(self,action):
        self.location = self.simulate_step(action)
        self.last_action = action


