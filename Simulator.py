
import matplotlib.pyplot as plt
def Simulatortext(grid,num_steps):
    agent1 = grid.agents[0]
    for _ in range(num_steps):
        current_location,last_location,reward,done = agent1.take_step()
        print('the agent location is %s'%(str(agent1.location)))
        print('the last action is %s'%(str(agent1.last_action)))
        print('the reward for the last action is %s'%(str(reward)))
        if done:
            break

def Simulatorgraphical(grid,num_steps=10,just_agents = False):
    agents = grid.agents
    done = False
    if just_agents== False:
        for _ in range(num_steps):
            plt.cla()
            for agent in agents:
                plt.imshow(agent.see_map())
            plt.show(block=False)
            plt.pause(.0005)
            for agent in agents:
                _,_,_,done= agent.take_step()
            if done:
                break
    else:
        for _ in range(num_steps):
            plt.cla()
            for agent in agents:
                plt.imshow(agent.grid.get_state_grid())
            plt.show(block=False)
            plt.pause(.0005)
            for agent in agents:
                _,_,_,done= agent.take_step()
            if done:
                print('you won!')
                break

if __name__ == '__main__':
    from Grid import Grid
    from agent import agent
    import Learner
    import numpy as np

    X, Y = np.meshgrid(np.linspace(0, 10, 10), np.linspace(0, 10, 10))
    Map = abs(X-5) + abs(Y-5)
    grid = Grid(Map = Map)
    plt.figure(1)
    grid.show_grid()
    plt.figure(2)
    grid.add_agent(learner='RandomFinder')
    grid.add_agent(learner = 'RandomFinder')
    #grid.add_agent(learner='RandomFinder')
    #grid.add_agent(learner='RandomFinder')
    #grid.add_agent(learner='RandomFinder')
    print('meeting point is %s' %(str(grid.agents[0].meeting_point)))
    Simulatorgraphical(grid,num_steps=100,just_agents=True)



