import networkx as nx
import json
from semanticscholar import SemanticScholar


def get_author_id_by_name(author_name: str):
    
    sch = SemanticScholar() # Library element to make API calls.
    
    # Name query may return many results; sort by H-index.
    results = sorted(sch.search_author(author_name), key=lambda x: -x["hIndex"])
    
    return results[0]["authorId"]

def get_coauthor_list(sch: object, author_id: int):
    
    author = sch.get_author(author_id) # Author API object.
    
    coauthors = set() # Will hold all coauthors; initialize to empty.

    if "papers" not in author.keys():
        return coauthors
    
    # Iterate through papers and add coauthors.
    for paper in author["papers"]:
        for author in paper["authors"]:
            if author["authorId"] != None and \
                int(author["authorId"]) != author_id:
                coauthors.add((int(author["authorId"]), author["name"]))

    return coauthors

def bfs(src_id: int, tgt_id: int):

    sch = SemanticScholar() # to make API calls.

    src = sch.get_author(src_id) # Source author.
    tgt = sch.get_author(tgt_id) # Target author.
    api_calls = 0 # Keep track of the number of API calls.

    # Initialize graph.
    G = nx.Graph()
    G.add_node(src["authorId"], 
        id=src["authorId"], 
        name=src["name"], 
        dist=0, 
        known="src")
    G.add_node(tgt["authorId"], 
        id=tgt["authorId"], 
        name=tgt["name"], 
        dist=0, 
        known="tgt")
    
    # Initialize queues to operate bfs and variables to keep track of distance.
    fwd_q, fwd_dist = [G.nodes[str(src_id)]], 0
    bwd_q, bwd_dist = [G.nodes[str(tgt_id)]], 0

    min_dist = 100 # Length of shortest path; initialize to big number.

    # Breadth first search.
    while True:
        
        # Pop node from queues; heuristics: pop node closest to source/target.
        if fwd_dist < bwd_dist:
            curr_node = fwd_q.pop(0)
            fwd_dist = curr_node["dist"]
            dir = "src"
            print("Branching FORWARD on {} at distance {}, id {}".format(curr_node["name"], fwd_dist, curr_node["id"]))
        
        else:
            curr_node = bwd_q.pop(0)
            bwd_dist = curr_node["dist"]
            dir = "tgt"
            print("Branching BACKWARD on {} at distance {}, id {}".format(curr_node["name"], bwd_dist, curr_node["id"]))

        # No more possible shortest paths. Halt.
        if fwd_dist + bwd_dist >= min_dist or \
            api_calls > 100: break # No more possible shortest paths. Halt.
        api_calls += 1
        
        # Iterate through list of coauthors.
        for author, name in get_coauthor_list(sch, int(curr_node["id"])):

            # Found a new node; add it to the graph.
            if G.nodes.get(str(author)) == None:

                # Create new node and edge.
                G.add_node(str(author), 
                    id=str(author), 
                    name=name, 
                    dist=curr_node["dist"] + 1, 
                    known=dir)
                G.add_edge(curr_node["id"], str(author))
                
                # Add new node to appropriate queue.
                if dir == "src": fwd_q.append(G.nodes[str(author)])
                else: bwd_q.append(G.nodes[str(author)])
            
            # Found a path from src to target: 
            elif (dir == "fwd" and G.nodes[str(author)]["known"] == "tgt") \
                or (dir == "tgt" and G.nodes[str(author)]["known"] == "fwd"):

                # Add edge.
                G.add_edge(curr_node["id"], str(author))

                # Update minimum distance path.
                min_dist = min(curr_node["dist"] + G.nodes[str(author)]["dist"] + 1, min_dist)
            
            # Already discovered node; just add edge.
            else:

                # Add edge.
                G.add_edge(curr_node["id"], str(author))
    return G

def simplify_graph(G: object, src_id: int, tgt_id: int):

    min_length = 100 # Shortest path length. Initialize to big number.
    paths = [] # Will hold all paths.
    name_paths = [] # Will hold paths, but with author names.
    nodes = [] # Will hold all nodes.
    known_nodes = set() # Avoid duplicate nodes.
    edge_pairs = set() # Store unique edges.
    edges = [] # Will hold all edges

    # Extract shortest paths and create new graph.
    for path in nx.shortest_simple_paths(G, str(src_id), str(tgt_id)):

        # Get only the shortest paths.
        min_length = min(min_length, len(path))
        if len(path) > min_length: break

        paths.append(path) # Shortest path; add to the list.
        name_paths.append(tuple([G.nodes[node]["name"] for node in path])) # Shortest path; add to the list.
        for i in range(len(path)):
            if path[i] in known_nodes: continue # Duplicate; skip.
            nodes.append({"id": path[i], # Add node.
                "name": G.nodes[path[i]]["name"], 
                "dist": i})
            known_nodes.add(path[i])


    for path in paths:
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) not in edge_pairs:
                edges.append({
                    "source": path[i], 
                    "target": path[i + 1]
                })
                edge_pairs.add((path[i], path[i + 1]))

    return {"edges": edges, 
        "nodes": nodes, 
        "paths": tuple(name_paths)}

def pipeline(src_author: str, tgt_author: str):

    # Get author ids from names.
    src_id = get_author_id_by_name(src_author) 
    tgt_id = get_author_id_by_name(tgt_author)

    G = bfs(src_id, tgt_id) # Run breadth first search and get the graph.
    return json.dumps(simplify_graph(G, src_id, tgt_id)) # Return simplified graph as json.