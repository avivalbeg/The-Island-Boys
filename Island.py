from scipy.spatial import Voronoi, voronoi_plot_2d
import random
import numpy as np
import matplotlib.pyplot as plt

def perlin(x,y,seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
    return lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y


def Lloyd(V):
    points = []

    for region in V.regions:
        L = [x for x in region if x != -1]
        if L != []:
            verts = V.vertices[L]
            point = 0
            for vert in verts:
                if vert[0] > 1000:
                    vert[0] = 1000
                if vert[0] < 0:
                    vert[0] = 0
                if vert[1] < 0:
                    vert[1] = 0
                if vert[1] > 1000:
                    vert[1] = 1000
                point += vert / len(verts)
            if type(point) == np.ndarray:
                points.append(point)
    return points

def Lloyds(n=200):
    points = 1000*np.random.rand(n,2)
    V = Voronoi(points)
    for _ in range(100):
        points = Lloyd(V)
        V = Voronoi(points)
    voronoi_plot_2d(Voronoi(points))
    plt.show()

if __name__ =='__main__':
    lin = np.linspace(0,5,200,endpoint=False)
    x,y = np.meshgrid(lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake

    terrain = perlin(x,y,seed=4)
    Lloyds()
    plt.imshow(terrain)
    plt.show()