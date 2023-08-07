'''
import sys
import os
from collections import deque
# Fixing imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import networkx as nx
from semantic_scholar_client import useSemanticScholar, getAuthorByName, getCoauthorList

client = useSemanticScholar()
src = getAuthorByName(client, "Thomas Bergamaschi")
tgt = getAuthorByName(client, "Christos Papadimitriou")

graph = nx.Graph()
graph.add_node(
    src.id, 
    dist=0
)
graph.add_node(
    tgt.id, 
    dist=0
)

fwd_queue = deque([(src, 0)])
bwd_queue = deque([(tgt, 0)])

# Visited sets for forward and backward BFS
fwd_visited = set([src.id])
bwd_visited = set([tgt.id])
dist_fwd = 0
dist_bwd = 0
min_dist = 100 # Big number.

while dist_fwd + dist_bwd < min_dist:

    # Forward BFS
    pop_fwd, dist_fwd = fwd_queue.popleft()
    print('popped fwd: {}'.format(pop_fwd.name))
    for neighbor in getCoauthorList(client, pop_fwd):
        if neighbor.id in fwd_visited:
            continue
        
        if neighbor.id not in bwd_visited:
            graph.add_node(
                neighbor.id, 
                dist=dist_fwd + 1
            )
            fwd_queue.append((neighbor, dist_fwd + 1))
        else:
            min_dist = min(
                min_dist, 
                dist_fwd + 1 + graph.nodes[neighbor.id]['dist']
            )
        # Add edge.
        graph.add_edge(pop_fwd.id, neighbor.id)
        fwd_visited.add(neighbor.id)

    # Forward BFS
    pop_bwd, dist_bwd = bwd_queue.popleft()
    print('popped bwd: {}'.format(pop_bwd.name))
    for neighbor in getCoauthorList(client, pop_bwd):
        if neighbor.id in bwd_visited:
            continue
        
        if neighbor.id not in fwd_visited:
            graph.add_node(
                neighbor.id, 
                dist=dist_bwd + 1
            )
            bwd_queue.append((neighbor, dist_bwd + 1))
        else:
            min_dist = min(
                min_dist, 
                dist_bwd + 1 + graph.nodes[neighbor.id]['dist']
            )
        # Add edge.
        graph.add_edge(pop_bwd.id, neighbor.id)
        bwd_visited.add(neighbor.id)

print("Total number of nodes: {}".format(len(graph.nodes)))
'''

import sys
import os
from collections import deque
# Fixing imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import networkx as nx
from semantic_scholar_client import useSemanticScholar, getAuthorByName, getCoauthorList, bfs

client = useSemanticScholar()
src = getAuthorByName(client, "Thomas Bergamaschi")
tgt = getAuthorByName(client, "Christos Papadimitriou")

bfs(client, src, tgt)