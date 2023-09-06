import json
from collections import deque
import networkx as nx
import logging
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from erdos.util.Graph import Graph
from erdos.util.Semantic_Scholar_Client import Semantic_Scholar_Client

async def index(request):

    if request.method != 'GET':
        return JsonResponse(
            {'error': 'method not allowed'},
            status=405
        )

    client = Semantic_Scholar_Client()
    src = await client.get_author_by_name(request.GET['src'])
    tgt = await client.get_author_by_name(request.GET['tgt'])

    print("hoe")
    logging.warning("Obtained src and tgt nodes.")

    '''
    except Exception as error:
        return JsonResponse({
            'error': 'Failed to find source or target authors.', 
            'exception': str(error)
            }, 
            status=200
        )
    '''
    
    graph = Graph(src=src, tgt=tgt)
    await graph.bfs()
    '''
    except Exception as error:
        print(error)
        return JsonResponse({
            'error': 'Failed to find paths connecting the authors.', 
            'exception': str(error)
            },
            status=200
        )
    '''

    return StreamingHttpResponse(
        graph.get_json(),
        content_type='application/json')

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