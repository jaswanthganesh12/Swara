from pydantic import BaseModel,HttpUrl


class Track(BaseModel):
    title: str
    id : str
    artist : str
    thumbnail : HttpUrl | None = None
    url : HttpUrl
    publishedAt : str | None = None
