import sys
import os
# Fixing imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import networkx as nx
from semanticscholar import SemanticScholar
from models.sample_models import Author
from collections import deque

def useSemanticScholar():

    key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
    return SemanticScholar(api_key=key)

def getAuthorByName(client, name):

    # Name query may return many results; sort by H-index.
    author = sorted(
        client.search_author(name), 
        key=lambda x: -x["hIndex"]
    )[0]
    
    return Author(
        id=author["authorId"], 
        name=author["name"]
    )

def getCoauthorList(client, author):

    authorApiObj = client.get_author(author.id) # Author API object.
    coauthors = [] # Will hold all coauthors; initialize to empty.

    if "papers" not in authorApiObj.keys():
        return coauthors
    
    # Iterate through papers and add coauthors.
    for paper in authorApiObj["papers"]:
        for coauthor in paper["authors"]:
            if coauthor["authorId"] != None and \
                int(coauthor["authorId"]) != author.id:
                coauthors.append(
                    Author(
                    id=coauthor["authorId"], 
                    name=coauthor["name"]
                ))

    return coauthors

def bfs(client, src, tgt):

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
    return graph

