from typing import Set
import environ
from semanticscholar import AsyncSemanticScholar
from erdos.pydantic_models import Author

# Load environment variables.
env = environ.Env()
environ.Env.read_env()

class Semantic_Scholar_Client:
    """Class to make calls to the Semantic Scholar API."""

    def __init__(self) -> AsyncSemanticScholar:

        self.client = AsyncSemanticScholar(
            api_key=env("SEMANTIC_SCHOLAR_API_KEY"),
            timeout=100
        )
        print(env("SEMANTIC_SCHOLAR_API_KEY"))

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

        return coauthors, len(author_api_obj["papers"])
