from queue import PriorityQueue
import networkx as nx
import numpy as np
import time

def dijkstra(G, s, t):
    #
    node_list = list(G.nodes)

    # 
    nvg        = node_list[-1] + 1
    dists      = [np.Inf for i in range(nvg)]
    parents    = [0 for i in range(nvg)]
    visited    = [False for i in range(nvg)]
    pathcounts = [0 for i in range(nvg)]
    preds      = [[] for i in range(nvg)]
    
    # check if nodes exists
    if not (s in G):
        raise Exception('source node not found in graph')
    
    if not (t in G):
        raise Exception('target node not found in graph')

    # priority queue
    H = PriorityQueue()
    for i in range(nvg):
        H.put((np.Inf, str(i)))

    # fill creates only one array.
    dists[s]      = 0.0
    visited[s]    = True
    pathcounts[s] = 1
    H.put((0.0, str(s)))

    # runs while queue has elements
    start_time = time.time()
    while not H.empty():

        # remove "cheapest" element
        next_item = H.get()
        
        # print(next_item)
        u = int(next_item[1])

        # stop criterium
        if u == t:
            break

        # Cannot be typemax if `u` is in the queue
        d = dists[u] 
        
        for v, _ in G.adj[u].items():

            alt = d + G.edges[u, v]['weight']

            if not(visited[v]):
                visited[v] = True
                dists[v]   = alt
                parents[v] = u
                pathcounts[v] += pathcounts[u]
                H.put((alt, str(v)))

            elif alt < dists[v]:
                dists[v] = alt
                parents[v] = u
                pathcounts[v] = pathcounts[u]
                H.put((alt, str(v)))

            elif alt == dists[v]:
                pathcounts[v] += pathcounts[u]
                
    print("--- %s seconds ---" % (time.time() - start_time))

    # 
    pathcounts[s] = 1
    parents[s]    = 0
    # preds.remove(s)

    return dists, parents

def get_dijkstra_path(parents, t):
    path = [t]
    while t != 0:
        t = parents[t]
        if t != 0:
            path.append(t)
    return path

# G = nx.Graph()
# G.add_weighted_edges_from([
#     # no, nd, we
#     (0, 1, 1.0),
#     (1, 2, 1.0),
#     (0, 2, 1.5),
#     (2, 3, 2.0)
# ])

# s=0
# t=3

# dijkstra(G, s, t)