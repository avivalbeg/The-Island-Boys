import networkx as nx
from scipy.spatial import distance_matrix as D
from Grid import Grid
import numpy as np
import matplotlib.pyplot as plt
class Graph:
    def __init__(self,grid):
        self.grid = grid
        self.Gr = nx.DiGraph()
        self.RECONNECT()

    def get_Dist_Mat(self):
        vecs = []
        for node in self.Gr.nodes:
            vecs.append(node.location)
        Dists = D(vecs,vecs)
        return Dists

    def connect(self,Dists):
        I, J = Dists.shape
        connected = np.zeros((I, J))
        nodes = list(self.Gr.nodes)
        for i in range(I):
            for j in range(J):
                if nodes[i].viewing > Dists[i, j] and i != j:
                    connected[i, j] = True
                    self.Gr.add_edge(nodes[i], nodes[j])

    def RECONNECT(self):
        self.Gr = nx.DiGraph()
        for i, agent in enumerate(self.grid.agents):
            self.Gr.add_node(agent, label=i)
        self.D = self.get_Dist_Mat()
        self.connect(self.D)

    def show_Graph(self):
        nx.draw(Gr.Gr)
        plt.show()





if __name__ == '__main__':
    G = Grid()
    G.add_agent([1,0],viewing = 3)
    G.add_agent([3,0],viewing = 3.3)
    G.add_agent([3,3])
    Gr = Graph(G)
    Gr.show_Graph()


    # from Grid import Grid
    # import numpy as np
    # G = Grid()
    # G.add_agent([1,0],viewing = 2)
    # G.add_agent([3,0])
    #
    # Gr = nx.Graph()
    # for i,agent in enumerate(G.agents):
    #     Gr.add_node(agent)
    # vecs = []
    # for node in Gr.nodes:
    #     vecs.append(node.location)
    # Dists = D(vecs,vecs)
    # I,J = Dists.shape
    # connected = np.zeros((I,J))
    # for i in range(I):
    #     for j in range(J):
    #         if list(Gr.nodes)[i].viewing>Dists[i,j] and i != j:
    #             connected[i,j] = True
    #             Gr.add_edge(i,j)
    # print(Gr.edges)


