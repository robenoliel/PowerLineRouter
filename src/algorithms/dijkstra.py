from cmath import inf
from queue import PriorityQueue
import networkx as nx

def dijkstra(G, s, t):

    nvg        = G.number_of_edges()
    dists      = [inf for i in range(nvg)]
    parents    = [0 for i in range(nvg)]
    visited    = [False for i in range(nvg)]
    pathcounts = [0 for i in range(nvg)]
    preds      = [[] for i in range(nvg)]
    
    # priority queue
    H = PriorityQueue()
    for i in range(nvg):
        H.put((i, inf))

    # fill creates only one array.
    dists[s]      = 0.0
    visited[s]    = True
    pathcounts[s] = 1
    H.put((s, 0.0))
    H.get()

    # runs while queue has elements
    while not H.empty():
        print("1. passou")

        # remove "cheapest" element
        next_item = H.get()
        print(next_item)
        u = next_item[0]

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
                H.put((v,alt))

            elif alt < dists[v]:
                dists[v] = alt
                parents[v] = u
                pathcounts[v] = pathcounts[u]
                H.put((v,alt))

            elif alt == dists[v]:
                pathcounts[v] += pathcounts[u]
                
    # 
    pathcounts[s] = 1
    parents[s]    = 0
    # preds.remove(s)

    return dists, parents