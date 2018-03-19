
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

def Simulatorgraphical(grid,num_steps=10,just_agents = False,individual_agents=True):
    agents = grid.agents
    done = False
    if just_agents== False:
        for _ in range(num_steps):
            plt.cla()
            for agent in agents:
                plt.imshow(agent.see_map())
            plt.show(block=False)
            plt.pause(.0005)
            for i,agent in enumerate(agents):
                print('this is agent %d'%i)
                _,_,_,done= agent.take_step()
            if done:
                break
    elif individual_agents:
        for i, agent in enumerate(agents):
            for _ in range(num_steps):
                plt.cla()
                plt.imshow(agent.grid.get_state_grid()+grid.pheremones+grid.Map/10000)
                #print(grid.pheremones)

                plt.show(block=False)
                plt.pause(.0005)
                _, _, _, done = agent.take_step()
                if done:
                    print('you won!')
                    break
                if agent.meeting_point[0]==agent.location[0] and agent.meeting_point[1]==agent.location[1]:
                    print('OK')
                    break

    else:

        for _ in range(num_steps):
            plt.cla()
            for agent in agents:
                plt.imshow(agent.grid.get_state_grid())
            plt.show(block=False)
            plt.pause(.0005)
            for i,agent in enumerate(agents):
                print('this is agent %d'%i)
                _,_,_,done= agent.take_step()
            if done:
                print('you won!')
                break

if __name__ == '__main__':
    from Grid import Grid
    from agent import agent
    import Learner
    import numpy as np
    import maze as maze
    #maze = maze.maze(100,100,complexity = .001,density=.1)
    X, Y = np.meshgrid(np.linspace(0, 10, 10), np.linspace(0, 10, 10))
    Map = maze
    Map = np.zeros((20,20))
    Map[1, 4] = 100000
    Map[2, 4] = 100000
    Map[3, 4] = 100000
    Map[4,4] = 100000
    Map[5,4] = 100000
    Map[6,4] = 100000
    Map[7,4] = 100000
    Map[8,3] = 100000
    Map[17,17] = 100000
    Map[17,18]=100000
    Map[18,17]=100000
    Map[18,16]=100000
    Map[16, 18] = 100000

    grid = Grid(Map = Map,meeting_point=[18,18])
    plt.figure(1)
    grid.show_grid()
    plt.figure(2)
    for _ in range(30):
        grid.add_agent(location=[3,1],learner='DynamicMCTSFinder',ant_mode = False)
    # grid.add_agent(location=[3, 1], learner='DynamicMCTSFinder',ant_mode = False)
    # grid.add_agent(location=[8,7],learner = 'DynamicMCTSFinder')
    #grid.add_agent(learner='RandomFinder')
    #grid.add_agent(learner='RandomFinder')
    #grid.add_agent(learner='RandomFinder')
    print('meeting point is %s' %(str(grid.agents[0].meeting_point)))
    #Simulatortext(grid, num_steps=100)
    Simulatorgraphical(grid,num_steps=100,just_agents=True)

