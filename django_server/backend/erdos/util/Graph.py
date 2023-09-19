import json
import time
import random
from collections import deque
import asyncio
import logging
import networkx as nx
from erdos.pydantic_models import Author
from erdos.util.Semantic_Scholar_Client import Semantic_Scholar_Client

class Graph:
    """Class to represent the coauthorship graph."""

    def __init__(
            self,
            src: Author,
            tgt: Author,
            timeout: float=0.02,
            max_neighbors: int=10
        ):

        self.src = src
        self.tgt = tgt

        self.src.dist = 0
        self.tgt.dist = 0

        self.frontier_src = deque([src])
        self.frontier_tgt = deque([tgt])

        self.visited_src = set([src.id])
        self.visited_tgt = set([tgt.id])

        self.graph = nx.Graph()
        self.simplified_graph = None
        self.add_node(src)
        self.add_node(tgt)

        self.min_dist = 100 # min distance path found. Initiate as big number.

        self.client = Semantic_Scholar_Client()

        self.timeout = timeout
        self.max_neighbors = max_neighbors

        self.num_papers = 0

    def add_node(self, author: Author) -> None:

        self.graph.add_node(
            author.id,
            dist=author.dist,
            author_obj=author
        )

    async def expand(self, src_or_tgt: str) -> None:

        logging.warning("Expanded")

        if src_or_tgt == "src":
            frontier = self.frontier_src
            visited = self.visited_src
            visited_opposite = self.visited_tgt
        if src_or_tgt == "tgt":
            frontier = self.frontier_tgt
            visited = self.visited_tgt
            visited_opposite = self.visited_src

        # Send concurrent calls to API, then wait for all to complete.
        promises = []
        for author in frontier:
            logging.warning("Frontier size = {}".format(len(frontier)))
            promise = self.client.get_coauthor_list(author=author)
            promises.append(promise)
            logging.warning("Made API call to get {} neighbors.".format(author.name))
            time.sleep(self.timeout) # Avoid going over limit of API calls.

        resolved_promises = await asyncio.gather(*promises, return_exceptions=True)

        for i in range(len(frontier)):
            author = frontier.popleft()

            # Failed author API call, just skip it.
            try:
                assert isinstance(resolved_promises[i][0], set)
            except AssertionError as error:
                logging.warning(
                    "API call to author '{}' failed, skipping. \n {}"\
                        .format(author.name, error)
                )
                continue
            except TypeError as error:
                logging.warning(
                    "API call to author '{}' failed, skipping. \n {}"\
                        .format(author.name, error)
                )
                continue
            
            # Add to number of papers scanned.
            self.num_papers += resolved_promises[i][1]

            for coauthor in random.sample(
                list(resolved_promises[i][0]), 
                min(len(resolved_promises[i][0]), self.max_neighbors)
            ):
                if coauthor.id in visited:
                    continue

                if coauthor.id not in visited_opposite:
                    visited.add(coauthor.id)
                    coauthor.dist = author.dist + 1
                    self.add_node(coauthor)
                    frontier.append(coauthor)
                else:
                    self.min_dist = min(
                        self.min_dist,
                        author.dist + 1 + coauthor.dist
                    )

                self.graph.add_edge(author.id, coauthor.id)

    async def bfs(self) -> None:

        depth = 0

        while depth < self.min_dist:
            await self.expand(src_or_tgt="src")
            await self.expand(src_or_tgt="tgt")
            depth += 2
            logging.warning(depth)
            yield "@" + json.dumps({
                "num_nodes": len(self.graph.nodes), 
                "num_papers": self.num_papers
            }) # @ character used to separate each chunk

        shortest_paths = list(nx.all_shortest_paths(
            self.graph,
            source=self.src.id,
            target=self.tgt.id
        ))
        new_graph = self.graph.subgraph(
            [node for path in shortest_paths for node in path]
        )

        self.simplified_graph = new_graph

        yield self.get_json()

    def get_json(self):

        return "@" + json.dumps({
            "num_nodes": len(self.graph.nodes), 
            "num_papers": self.num_papers,
            "nodes": [self.simplified_graph.nodes[key]['author_obj'].model_dump_json() 
                        for key in list(self.simplified_graph.nodes.keys())],
            "edges": [{
                'source': self.simplified_graph.nodes[pair[0]]['author_obj'].model_dump_json(), 
                'target': self.simplified_graph.nodes[pair[1]]['author_obj'].model_dump_json()
            } for pair in list(self.simplified_graph.edges.keys())]
    })
            