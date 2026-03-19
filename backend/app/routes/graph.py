from fastapi import APIRouter
from app.models.schemas import GraphResponse, GraphNode, GraphEdge
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=GraphResponse)
async def get_graph(limit: int = 100):
    async with get_db() as db:
        db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        nodes_raw = await db.execute_fetchall(
            "SELECT id, url, title, rank_score FROM pages ORDER BY rank_score DESC LIMIT ?",
            (limit,),
        )
        node_ids = {r["id"] for r in nodes_raw}
        edges_raw = await db.execute_fetchall(
            "SELECT source_id, target_id FROM links",
        )

    nodes = [
        GraphNode(id=r["id"], url=r["url"], title=r["title"] or r["url"], rank_score=r["rank_score"])
        for r in nodes_raw
    ]
    edges = [
        GraphEdge(source=r["source_id"], target=r["target_id"])
        for r in edges_raw
        if r["source_id"] in node_ids and r["target_id"] in node_ids
    ]

    return GraphResponse(nodes=nodes, edges=edges)