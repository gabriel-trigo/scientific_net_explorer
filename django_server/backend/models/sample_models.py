from typing import Set
from pydantic import BaseModel

class Author(BaseModel):
    id: str
    name: str
    coauthors: Set['Author'] = set()