from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from app.database import init_db
from app.routes import crawl, search, graph

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Lav-oogle",
    description="A mini search engine with real PageRank. 🔍",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crawl.router,  prefix="/crawl",  tags=["crawl"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(graph.router,  prefix="/graph",  tags=["graph"])


@app.get("/")
async def root():
    return {"message": "Lav-oogle is running 🔍"}