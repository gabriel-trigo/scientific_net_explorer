import networkx as nx
import json
from collections import deque
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from models.sample_models import Author
from util.semantic_scholar_client import useSemanticScholar, getAuthorByName, getCoauthorList

def bfs(client, src, tgt):

    graph = nx.Graph()
    graph.add_node(
        src.id, 
        dist=0, 
        authorObj=src
    )
    graph.add_node(
        tgt.id, 
        dist=0, 
        authorObj=tgt
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
        print(pop_fwd)

        try:
            coauthorList = getCoauthorList(client, pop_fwd)
        except:
            coauthorList = []

        for neighbor in coauthorList:
            if neighbor.id in fwd_visited:
                continue
            
            if neighbor.id not in bwd_visited:
                graph.add_node(
                    neighbor.id, 
                    dist=dist_fwd + 1, 
                    authorObj=neighbor
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
        print(pop_bwd)

        try:
            coauthorList = getCoauthorList(client, pop_bwd)
        except:
            coauthorList = []

        for neighbor in coauthorList:
            if neighbor.id in bwd_visited:
                continue
            
            if neighbor.id not in fwd_visited:
                graph.add_node(
                    neighbor.id, 
                    dist=dist_bwd + 1, 
                    authorObj=neighbor
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
        
        yield "@" + json.dumps({
            "num_nodes": len(graph.nodes)
        }) # @ character used to separate each chunk

    print("Total number of nodes: {}".format(len(graph.nodes)))

    shortest_paths = list(nx.all_shortest_paths(graph, source=src.id, target=tgt.id))
    new_graph = graph.subgraph([node for path in shortest_paths for node in path])

    yield "@" + json.dumps({
            "num_nodes": len(graph.nodes), 
            "nodes": [new_graph.nodes[key]['authorObj'].model_dump_json() 
                        for key in list(new_graph.nodes.keys())], 
            "edges": [{
                'source': new_graph.nodes[pair[0]]['authorObj'].model_dump_json(), 
                'target': new_graph.nodes[pair[1]]['authorObj'].model_dump_json()
            } for pair in list(new_graph.edges.keys())]
    })

    return new_graph

def index(request):

    if request.method != 'GET':
        return JsonResponse({'error': 'method not allowed'}, status=400)
    
    try: 
        client = useSemanticScholar()
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to connect to Semantic Scholar API', 
            'exception': str(e)
        }, status=200)
    
    try:
        src = getAuthorByName(client, request.GET['src'])
        tgt = getAuthorByName(client, request.GET['tgt'])

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to find source or target authors.', 
            'exception': str(e)
        }, status=200)
    
    return StreamingHttpResponse(
        bfs(client, src, tgt), 
        content_type='application/json')