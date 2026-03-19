from pydantic import BaseModel, HttpUrl
from typing import Optional


class CrawlRequest(BaseModel):
    seed_url: HttpUrl
    max_depth: int = 2
    max_pages: int = 50


class CrawlStatus(BaseModel):
    pages_crawled: int
    links_found: int
    pagerank_computed: bool


class SearchResult(BaseModel):
    id: int
    url: str
    title: Optional[str]
    snippet: str
    rank_score: float
    fts_score: float
    combined_score: float


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult]


class GraphNode(BaseModel):
    id: int
    url: str
    title: Optional[str]
    rank_score: float


class GraphEdge(BaseModel):
    source: int
    target: int


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]