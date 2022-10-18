import networkx as nx

def surroundings(W,i,j,N,M,k):
    w = []
    for u in range(i,max(i+k,N)):
        for v in range(i,max(j+k,M)):
            w.append((u,v,W[u][v]))
    return w


def matrix_to_weighted_graph(W, K=1):

    # matrix dimension
    N = len(W)
    M = len(W[1])

    # graph initialization
    # should we define a DiGraph?
    G = nx.Graph()

    # getting weighted edges from matrix neighborhood 
    e = []
    for i in range(0,N):
        for j in range(0,M):            
            for k in range(0,K):
                e.append(surroundings(W,i,j,N,M,k))

    # setting edges (should be more efficient like this)
    G.add_weighted_edges_from(e)
   
    return G

def path_to_shape(path):
    shape = 0 # shapefile
    return shape