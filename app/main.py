from fastapi import FastAPI 
from api.routes.search import router as search_router



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

app.include_router(search_router)

