from fastapi import FastAPI 
from fastapi import Query


app = FastAPI(
    title = "Swara API",
    description = "backend for our music discovery app",
    version ="0.1.0",


)

@app.get("/")
def home():
    return {
        "message": "welcome to swara",
        "status": "running"
    }

@app.get("/api/v1/search")
async def search_tracks(
    q: str = Query(min_length=1, max_length=100),
    limit: int=Query(ge=1 , le=25),

):

    return{
        "query": q,
        "limit": limit,
        "message": "search endpoint is ready ",
        "tracks": [],
    }