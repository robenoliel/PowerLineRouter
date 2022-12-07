import networkx as nx
import numpy as np
import math
import time

def get_element(matrix, pos):
    """
    Returns element in `pos` position from numpy array. Parameters:
        matrix: Matrix (numpy array)
        pos: Matrix position (int)
    """
    coords = get_coords_from_pos(pos, matrix.shape)
    return matrix[coords[0], coords[1]]

def get_pos_from_coords(coords, size):
    """
    Returns element number position according to (x,y) tuple. Parameters:
        coords: Matrix coordinates (x,y) (int)
        size: Matrix order (m,n) (int)
    """
    if coords[0] > size[0] or coords[1] > size[1]:
        raise Exception('Index out of range')
    return (coords[0] - 1)*size[1] + coords[1]

def get_coords_from_pos(pos, size):
    """
    Returns element coordinates according to position number. Parameters:
        pos: Matrix position (int)
        size: Matrix order (m,n) (int)
    """
    if pos > size[0]*size[1]:
        raise Exception('Index out of range')

    row, col = math.ceil(pos / size[1]) - 1, pos % size[1] - 1

    if (col < 0): col += size[1]

    return (row, col)

def mean(x):
    return sum(x)/len(x)


def surroundings(W,i,j,N,M):
    w = []
    for u in range(i,min(i+1,N)):
        for v in range(i,min(j+1,M)):
            w.append((u, v, mean([W[i,j], W[u][v]])))
    return w


def matrix_to_weighted_graph(W):
        
    # matrix dimension
    N, M = W.shape

    # graph initialization
    # should we define a DiGraph?
    G = nx.Graph()
    G.add_nodes_from(range(N*M))

    # node map
    O = make_node_map(N, M)

    # getting weighted edges from matrix neighborhood 
    start_time = time.time()
    for i in range(0,N):
        for j in range(0,M):

            # east
            if j+1 < M:
                G.add_edge(O[i,j], O[i,j+1], weight=mean([W[i,j], W[i,j+1]]))

            # south-east
            if (i+1 < N) & (j+1 < M):
                G.add_edge(O[i,j], O[i+1,j+1], weight=mean([W[i,j], W[i+1,j+1]]) * 1.41)

            # south
            if (i+1 < N):
                G.add_edge(O[i,j], O[i+1,j], weight=mean([W[i,j], W[i+1,j]]))
            
            # south-west
            if (i+1 < N) & (j-1 > 0):
                G.add_edge(O[i,j], O[i+1,j-1], weight=mean([W[i,j], W[i+1,j-1]]) * 1.41)

    print("--- %s seconds ---" % (time.time() - start_time))

    return G, O

def make_node_map(N, M, zero_based=True):
    node_map = np.zeros((N, M), dtype=int)
    
    k = 0
    for i in range(N):
        for j in range(M):
            if not(zero_based): k += 1
            node_map[i,j] = k
            if zero_based: k += 1 

    return node_map


def path_to_shape(path):
    shape = 0 # shapefile
    return shape