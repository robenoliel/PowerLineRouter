import networkx as nx
import numpy as np

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
    return (pos // size[1] + 1, pos % size[1])

def mean(x):
    return sum(x)/len(x)


def surroundings(W,i,j,N,M,k):
    w = []
    for u in range(i,min(i+k+1,N)):
        for v in range(i,min(j+k+1,M)):
            w.append((u, v, mean([W[i][j], W[u][v]]) * k))
    return w


def matrix_to_weighted_graph(W, K=1):

    # matrix dimension
    N = len(W)
    M = len(W[1])

    # graph initialization
    # should we define a DiGraph?
    G = nx.Graph()

    # node map
    O = make_node_map(N, M)

    # getting weighted edges from matrix neighborhood 
    e = []
    for i in range(N):
        for j in range(M):            
            for k in range(K,K+1):
                for (u,v,w) in surroundings(W,i,j,N,M,k):
                    e.append( (O[i][j], O[u][v], w) )

    # setting edges (should be more efficient like this)
    G.add_weighted_edges_from(e)
   
    return G, O

def make_node_map(N, M):
    node_map = np.zeros((N, M), dtype=int)
    
    k = 0
    for i in range(N):
        for j in range(M):
            k += 1
            node_map[i][j]  = k

    return node_map


def path_to_shape(path):
    shape = 0 # shapefile
    return shape