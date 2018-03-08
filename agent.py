import numpy as np
from copy import deepcopy
#from Grid import Grid
import matplotlib.pyplot as plt
import Learner
from scipy.spatial import distance_matrix as distance

class agent:
    """
    represented by a dot they agents are trying to meet in the center
    """

    def __init__(self,grid,location = None,probabilities = None,learner = 'Random'):
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
        #self.meeting_point = None
        self.meeting_point = self.grid.meeting_point  # Just for now before I figure out how to get the robots to agree on a meeting spot.
        self.waiting = False
        self.viewing = 1
        self.view = np.zeros(grid.Map.shape,dtype=bool)
        if learner =='Random':
            self.brain = Learner.Random(self)
        if learner =='Manual':
            self.brain = Learner.Manual(self)
        if learner == 'RandomFinder':
            self.brain = Learner.RandomFinder(self)

    def convert_location_to_state(self):
        n = self.grid.size1
        s = (n-1)*self.location[0]+self.location[1]
        return s

    def communicate(self,message = 'm'):
        """

        :param message:'m' - change meeting point to ...
        Then wait for confirmation or a different opinion if the meeting point doesn't make sense to the second robot
        'a' - accept meeting point
        :return:
        """
        total_view = self.view
        for agent in self.grid.agents:
            total_view += agent.view
        for agent in self.grid.agents:
            agent.view = total_view
        if message == 'm':
            for agent in self.grid.agents:
                #agent.message = self.grid.get_new_meeting()
                pass

    def see_map(self):
        Map = self.grid.Map
        maxX,maxY = Map.shape
        x,y = self.location
        if x-self.viewing<0:
            xlow = 0
        else:
            xlow = x-self.viewing
        if y-self.viewing<0:
            ylow = 0
        else:
            ylow = y-self.viewing
        if x+self.viewing>maxX:
            xmax = maxX
        else:
            xmax = x+self.viewing
        if y+self.viewing>maxY:
            ymax = maxY
        else:
            ymax = y+self.viewing
        self.view[xlow:xmax,ylow:ymax] = True
        return self.view*Map

    def simulate_step(self,action = None,loc = None, probability = 1):
        done = False
        if action == None:
            action = self.brain.get_action()
        if loc ==None:
            loc = self.location
        last_loc = deepcopy(loc)
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
        if action ==5:
            pass  #self.communicate()
        if action ==6:
            pass  #self.communicate()
        if loc[0]<=0:
            loc[0]=0
        if loc[1]<=0:
            loc[1]=0
        if loc[0]>self.grid.size1-1:
            loc[0]=self.grid.size1-1
        if loc[1]>self.grid.size1-1:
            loc[1]=self.grid.size1-1


        #### The reward
        r = 0  # total reward for step
        k = 50 # Gain on distance
        k2 = -.2  # Gain on the gradient
        if self.meeting_point is None:
            r += -1
        else:
            r += k / (distance([self.location], [self.meeting_point]).squeeze() + 1)
        if action == None:
            action = self.last_action
        if action == 6:
            r -= .03
        elif action == 5:
            r -= .03
        elif action == 4:
            r += -.01
        else:
            r += -.03
        if self.grid.have_met() == True:
            r += 50
            done = True
        r_fromgrad = k2*(self.grid.Map[loc[0],loc[1]])
        #print('The reward from the gradient is %f'%r_fromgrad)
        r+= r_fromgrad    #The gradient contribution to the reward
        return loc,action,r,done


    def take_step(self,action=None):
        self.location,action,reward,done = self.simulate_step(action)
        self.last_action = action
        return self.location,action,reward,done

if __name__ =='__main__':
    from Grid import Grid
    import time
