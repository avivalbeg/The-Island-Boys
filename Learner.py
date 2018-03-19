import numpy as np
from copy import deepcopy
import operator
### This is a work in progress. The purpose of this file is as a general purpose MDP solver. Something that is surprisingly hard to find in a usable form in python.

class Manual:
    def __init__(self,agent):
        self.nA = agent.nA

    def get_action(self):
        OK = False
        while not OK:
            action = input('input an action')
            try:
                action = int(action)
                OK = True
            except:
                print('not an integer. Try again.')
        return action

class Random:
    def __init__(self,agent):
        self.nA = agent.nA

    def get_action(self):
        return np.random.randint(self.nA)

class RandomFinder:
    def __init__(self,agent,dynamic = False):
        self.agent = agent
        self.grid = agent.grid
        self.nA = agent.nA
        self.nS = agent.grid.size1**2
        self.Q = {}
        self.dynamic = dynamic
        self.done= False
        if dynamic:
            self.num_episodes = 500
            self.num_steps = 2
            self.dispersion = .3
            self.finalA = None


    def Search(self,num_episodes = 2000,num_steps = 2):
        self.Q = {}
        tot_count = 0
        for _ in range(num_episodes):
            Cagent = deepcopy(self.agent)
            r = 0
            A = ''
            for _ in range(num_steps):
                a = np.random.randint(0,self.nA)
                _,a,rn,done = Cagent.take_step(a)
                r+=rn
                A += str(a)
                if done:
                    print('found way home')
                    self.done = done
                    self.finalA = A
                    return A
            if A in self.Q:
                pass
            else:
                self.Q[A] = r
        A = max(self.Q.items(), key=operator.itemgetter(1))[0]
        return A


    def dynamic_Search(self):
        if not self.done:
            A = self.Search(num_episodes=self.num_episodes,num_steps=self.num_steps)
            waits = A.count('4')
        if self.done:
            if self.finalA is not None:
                A = self.finalA
                self.finalA = self.finalA[:-1]
            else:
                A = '4'
            return A
        else:
            A = self.Search(num_episodes=self.num_episodes, num_steps=self.num_steps)
            waits = A.count('4')
            if waits/self.num_steps>.5:
                self.num_steps+=1
                self.num_episodes = 4 ** (self.num_steps + 1)
                if self.num_episodes>500:
                    self.num_episodes=500
            else:
                if self.num_steps>1:
                    self.num_steps-=1
                    self.num_episodes=4**(self.num_steps+1)
                    if self.num_episodes > 500:
                        self.num_episodes = 500
            print('num steps: %d , num_episodes: %d'%(self.num_steps,self.num_episodes))
            return A

    def get_action(self):
        if not self.dynamic:
            A = self.Search()
        else:
            A = self.dynamic_Search()
        action = int(A[0])
        return action

class MCTSFinder:
    def __init__(self,agent,dynamic = False):
        self.agent = agent
        self.grid = agent.grid
        self.nA = agent.nA
        self.nS = agent.grid.size1**2
        self.Q = {}
        self.N = {}
        self.gamma = .6
        self.dynamic = dynamic
        self.done= False
        if dynamic:
            self.num_episodes = 16
            self.num_steps = 2
            self.dispersion = .3
            self.finalA = None
        else:
            self.num_steps = 2


    def Search(self,num_episodes = 2000,num_steps = 2):
        self.Q = {}
        self.N = {}
        tot_count = 0
        c=1
        self.num_episodes = 4 ** (self.num_steps + 1)
        for _ in range(num_episodes):
            Cagent = deepcopy(self.agent)
            r = 0
            A = ''
            for i in range(num_steps):
                a = np.random.randint(0,self.nA)
                loc,a,rn,done = Cagent.take_step(a)
                self.update_map()
                r+=(self.gamma**(i))*rn
                A += str(a)
                if A in self.Q:
                    self.N[A] +=1
                    self.Q[A] = self.Q[A]+(r-self.Q[A])/(self.N[A])+Cagent.knowledge[loc[0],loc[1]]+self.grid.pheremones[loc[0],loc[1]]
                else:
                    self.N[A] = 1
                    self.Q[A] = r

        A = max(self.Q.items(), key=operator.itemgetter(1))[0]
        return A


    def dynamic_Search(self):
        # if not self.done:
        #     A = self.Search(num_episodes=self.num_episodes,num_steps=self.num_steps)
        #     waits = A.count('4')
        if self.done:
            if self.finalA is not None:
                A = self.finalA
                self.finalA = self.finalA[:-1]
            else:
                A = '4'
            return A
        else:
            A = self.Search(num_episodes=self.num_episodes, num_steps=self.num_steps)
            waits = A.count('4')
            if waits/self.num_steps>.5:
                self.num_steps+=1
                self.num_episodes = 4 ** (self.num_steps+1)
                if self.num_episodes>500:
                    self.num_episodes=500
            else:
                if self.num_steps>4:
                    for elem in A:
                        self.agent.take_step(int(elem))
                        self.num_steps =1
                        self.num_episodes = 4**(self.num_steps+1)
                elif self.num_steps>1:
                    self.num_steps-=len(A)-A.count('4')-1
                    self.num_episodes=4**(self.num_steps+1)
                    if self.num_episodes > 500:
                        self.num_episodes = 500
            print('num steps: %d , num_episodes: %d'%(self.num_steps,self.num_episodes))
            return A

    def update_map(self):
        self.agent.knowledge[self.agent.location[0],self.agent.location[1]]+=-1



    def get_action(self):
        if not self.dynamic:
            A = self.Search()
        else:
            A = self.dynamic_Search()
        action = int(A[0])
        return action





class BFSFinder:
    def __init__(self):
        pass

class DFSFinder:
    def __init__(self):
        pass

class SARSA:
    def __init__(self, W, alpha=1, gamma=.95, lamda=.5):
        self.W = W
        self.nA = W.nA
        self.nS = W.nS
        self.nO = W.nO
        self.Q = np.zeros((self.nS, self.nA, self.nO))
        self.c_loc = W.location
        self.c_belief = W.belief
        self.alpha = alpha
        self.gamma = gamma
        self.lamda = .5

    def get_reward(self, location):
        return self.W.Grid.grid[location]

    def get_states(self, action):
        prev_location = self.c_loc
        prev_belief = self.c_belief
        current_location, current_belief, reward = self.W.take_action(action)
        if prev_location == 9 or prev_location == 0:
            prev_location = 4
            prev_belief = 0
        self.c_loc = current_location
        self.c_belief = current_belief
        return prev_location, prev_belief, current_location, current_belief, reward

    def choose_action(self, epsilon=.95):
        if np.random.rand() > epsilon:
            action = np.random.randint(0, 3)
            # print(action)
        else:

            action = np.argmax(self.Q[self.c_loc, :, self.c_belief])
            # print(action)
        return action

    def update_Q(self, r, action, next_action, prev_location, prev_belief, current_location, current_belief):

        self.Q[prev_location, action, prev_belief] = self.Q[prev_location, action, prev_belief] + self.alpha * (
                    r + self.gamma * self.Q[current_location, next_action, current_belief] - self.Q[
                prev_location, action, prev_belief])

    def learn(self, num_episodes=1000, max_steps=50):
        for _ in range(num_episodes):
            action = 2
            for _ in range(max_steps):
                prev_location, prev_belief, current_location, current_belief, r = self.get_states(action)
                next_action = self.choose_action()
                self.update_Q(r, action, next_action, prev_location, prev_belief, current_location, current_belief)
                action = next_action
                if r != 0:
                    if r < 0:
                        pass
                    #                         print('bad')
                    if r > 0:
                        #                         print('good')
                        break

    def make_readable(self, state, belief):
        T = np.argmax(self.Q[state, :, belief])
        if belief == 0:
            d = 'no belief'
        if belief == 1:
            d = 'bad is on left'
        if belief == 2:
            d = 'bad is on right'

        if T == 0:
            print(
                'if you are in state %d and you believe that %s then the best action is to take left' % (state, d))
        if T == 1:
            print('if you are in state %d and you believe that %s then the best action is to go right' % (state, d))
        if T == 2:
            print('if you are in state %d and you believe that %s then the best action is to listen' % (state, d))

    def make_full_readable(self):
        for i in range(self.nS):
            for j in range(self.nO):
                print(self.make_readable(i, j))

class SARSALambda:
    def __init__(self, W, alpha=1, gamma=.95, lamda=.5):
        self.W = W
        self.nA = W.nA
        self.nS = W.nS
        self.nO = W.nO
        self.Q = np.zeros((self.nS, self.nA, self.nO))
        self.c_loc = W.location
        self.c_belief = W.belief
        self.alpha = alpha
        self.gamma = gamma
        self.lamda = .5
        self.N = np.zeros((self.nS, self.nA, self.nO))

    def get_reward(self, location):
        return self.W.Grid.grid[location]

    def get_states(self, action):
        prev_location = self.c_loc
        prev_belief = self.c_belief
        current_location, current_belief, reward = self.W.take_action(action)
        if prev_location == 9 or prev_location == 0:
            prev_location = 4
            prev_belief = 0
        self.c_loc = current_location
        self.c_belief = current_belief
        return prev_location, prev_belief, current_location, current_belief, reward

    def choose_action(self, epsilon=.95):
        if np.random.rand() > epsilon:
            action = np.random.randint(0, 3)
            # print(action)
        else:

            action = np.argmax(self.Q[self.c_loc, :, self.c_belief])
            # print(action)
        return action

    def update_Q(self, r, action, next_action, prev_location, prev_belief, current_location, current_belief):
        delta = r + self.gamma * self.Q[current_location, next_action, current_belief] - self.Q[
            prev_location, action, prev_belief]
        self.N[prev_location, action, prev_belief] += 1
        for s in range(self.nS):
            for a in range(self.nA):
                for o in range(self.nO):
                    self.Q[s, a, o] = self.Q[s, a, o] + self.alpha * delta * self.N[s, a, o]
                    self.N[s, a, o] = self.gamma * self.lamda * self.N[s, a, o]

    def learn(self, num_episodes=1000, max_steps=50):
        for _ in range(num_episodes):
            action = 2
            for _ in range(max_steps):
                prev_location, prev_belief, current_location, current_belief, r = self.get_states(action)
                next_action = self.choose_action()
                self.update_Q(r, action, next_action, prev_location, prev_belief, current_location, current_belief)
                action = next_action
                if r != 0:
                    if r < 0:
                        pass
                    #                         print('bad')
                    if r > 0:
                        #                         print('good')
                        break

    def make_readable(self, state, belief):
        T = np.argmax(self.Q[state, :, belief])
        if belief == 0:
            d = 'no belief'
        if belief == 1:
            d = 'bad is on left'
        if belief == 2:
            d = 'bad is on right'

        if T == 0:
            print('if you are in state %d and you believe that %s then the best action is to take left' % (state, d))
        if T == 1:
            print('if you are in state %d and you believe that %s then the best action is to go right' % (state, d))
        if T == 2:
            print('if you are in state %d and you believe that %s then the best action is to listen' % (state, d))

    def make_full_readable(self):
        for i in range(self.nS):
            for j in range(self.nO):
                print(self.make_readable(i, j))

class QLearning:
    def __init__(self,W,alpha=1,gamma=.95):
        self.W = W
        self.nA = W.nA
        self.nS = W.nS
        self.nO = W.nO
        self.Q = np.zeros((self.nS,self.nA,self.nO))
        self.c_loc = W.location
        self.c_belief = W.belief
        self.alpha = alpha
        self.gamma = gamma

    def get_reward(self,location):
        return self.W.Grid.grid[location]

    def get_states(self,action):
        prev_location=self.c_loc
        prev_belief = self.c_belief
        current_location,current_belief,reward = self.W.take_action(action)
        if prev_location == 9 or prev_location == 0:
            prev_location =4
            prev_belief = 0
        self.c_loc = current_location
        self.c_belief = current_belief
        return prev_location,prev_belief,current_location,current_belief,reward

    def choose_action(self, epsilon=.5):
        if np.random.rand() > epsilon:
            action = np.random.randint(0, 3)
            # print(action)
        else:

            action = np.argmax(self.Q[self.c_loc, :, self.c_belief])
            # print(action)
        return action

    def update_Q(self, r, action,prev_location,prev_belief,current_location,current_belief):
        current_location = current_location
        current_belief = current_belief
        self.Q[prev_location, action, prev_belief] = self.Q[prev_location, action, prev_belief] + self.alpha * (
                                                                           r + self.gamma * max(
                                                                       self.Q[current_location, :, current_belief]) -
                                                                           self.Q[
                                                                               prev_location, action, prev_belief])

    def learn(self,num_episodes=1000,max_steps= 50):
        for _ in range(num_episodes):
            for _ in range(max_steps):
                action = self.choose_action()
                prev_location,prev_belief,current_location,current_belief, r = self.get_states(action)
                self.update_Q(r, action,prev_location,prev_belief,current_location,current_belief)
                if r!=0:
                    if r <0:
                        pass
#                         print('bad')
                    if r>0:
#                         print('good')
                        break

    def make_readable(self, state, belief):
        T = np.argmax(self.Q[state, :, belief])
        if belief == 0:
            d = 'no belief'
        if belief == 1:
            d = 'bad is on left'
        if belief == 2:
            d = 'bad is on right'

        if T == 0:
            print('if you are in state %d and you believe that %s then the best action is to take left' % (state, d))
        if T == 1:
            print('if you are in state %d and you believe that %s then the best action is to go right' % (state, d))
        if T == 2:
            print('if you are in state %d and you believe that %s then the best action is to listen' % (state, d))

    def make_full_readable(self):
        for i in range(self.nS):
            for j in range(self.nO):
                print(self.make_readable(i, j))

class QMDP:
    def __init__(self):
        pass
