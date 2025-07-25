from pydantic import BaseModel


class Post(BaseModel):
    slug: str
    contents: str
