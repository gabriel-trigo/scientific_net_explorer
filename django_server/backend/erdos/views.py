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
    try:
        src = await client.get_author_by_name(request.GET['src'])
        tgt = await client.get_author_by_name(request.GET['tgt'])
    except IndexError:
        print("hey")
        return JsonResponse(
            { "error": "Could not find source/target authors." },
            status=404
        )
    except Exception:
        return JsonResponse(
            { "error": "Unexpected error when searching source/target authors" },
            status=500
        )

    graph = Graph(src=src, tgt=tgt)

    return StreamingHttpResponse(
        graph.bfs())
