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

    return JsonResponse({'value': [Author(id='123', name='1,2,3').model_dump_json()]})
    
    try:
        src = getAuthorByName(client, "Thomas Bergamaschi")
        tgt = getAuthorByName(client, "Christos Papadimitriou")

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to find source or target authors.', 
            'exception': str(e)
        }, status=400)
    
    try:
        graph = bfs(client, src, tgt)
        return JsonResponse({'size': len(graph.nodes)})

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to find shortest paths.', 
            'exception': str(e)
        }, status=400)