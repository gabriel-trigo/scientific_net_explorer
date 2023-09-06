from typing import Set, Optional
from pydantic import BaseModel

class Author(BaseModel):
    """Class to represent an author."""

    id: str
    name: str
    coauthors: Set['Author'] = set()
    dist: Optional[int] = 0
