import os
from typing import Set
from semanticscholar import AsyncSemanticScholar
from erdos.pydantic_models import Author

class Semantic_Scholar_Client:
    """Class to make calls to the Semantic Scholar API."""

    def __init__(self) -> AsyncSemanticScholar:

        self.client = AsyncSemanticScholar(
            api_key=os.getenv('SEMANTIC_SCHOLAR_API_KEY'), 
            timeout=100
        )

    async def get_author_by_name(self, author_name: str) -> Author:

        author = sorted(
            await self.client.search_author(author_name),
            key=lambda x: -x["hIndex"]
        )[0]

        return Author(
            id=author["authorId"],
            name=author["name"],
            dist=0
        )

    async def get_coauthor_list(self, author: Author) -> Set[Author]:

        author_api_obj = await self.client.get_author(author.id)
        coauthors = set()

        # Author doesn't have any papers.
        if "papers" not in author_api_obj.keys():
            return coauthors

        # Iterate through all papers and find coauthors.
        for paper in author_api_obj["papers"]:
            for coauthor in paper["authors"]:
                if coauthor["authorId"] is not None and \
                    int(coauthor["authorId"]) != author.id:
                    coauthors.add(
                        Author(
                            id=coauthor["authorId"],
                            name=coauthor["name"]
                        ))

        return coauthors

'''
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

    print("Total number of nodes: {}".format(len(graph.nodes)))

    shortest_paths = list(nx.all_shortest_paths(graph, source=src.id, target=tgt.id))
    new_graph = graph.subgraph([node for path in shortest_paths for node in path])

    return new_graph
'''
