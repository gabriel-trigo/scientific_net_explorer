import os
from django.shortcuts import render
from django.http import JsonResponse
from models.sample_models import Author
from util.semantic_scholar_client import useSemanticScholar, getAuthorByName, bfs

def index(request):

    if request.method != 'GET':
        return JsonResponse({'error': 'method not allowed'}, status=400)
    
    try: 
        client = useSemanticScholar()
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to connect to Semantic Scholar API', 
            'exception': str(e)
        }, status=400)
    
    try:
        src = getAuthorByName(client, "Thomas Bergamaschi")
        tgt = getAuthorByName(client, "Tim Menke")

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to find source or target authors.', 
            'exception': str(e)
        }, status=400)
    
    try:
        graph = bfs(client, src, tgt)
        return JsonResponse({
            'nodes': [graph.nodes[key]['authorObj'].model_dump_json() 
                        for key in list(graph.nodes.keys())], 
            'edges': [{
                'source': graph.nodes[pair[0]]['authorObj'].model_dump_json(), 
                'dest': graph.nodes[pair[1]]['authorObj'].model_dump_json()
            } for pair in list(graph.edges.keys())]
        })

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to find shortest paths.', 
            'exception': str(e)
        }, status=400)