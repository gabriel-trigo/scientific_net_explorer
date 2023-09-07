import logging
import time
import asyncio
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

    logging.warning("Obtained src and tgt nodes.")

    graph = Graph(src=src, tgt=tgt)

    return StreamingHttpResponse(
        graph.bfs())
