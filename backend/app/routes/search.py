from fastapi import APIRouter, Query
from app.models.schemas import SearchResponse, SearchResult
from app.database import get_db

router = APIRouter()

SNIPPET_LEN = 200


def make_snippet(content: str, query: str) -> str:
    q_lower = query.lower()
    idx = content.lower().find(q_lower.split()[0]) if query else -1
    start = max(0, idx - 60) if idx != -1 else 0
    return content[start : start + SNIPPET_LEN].strip() + "…"


@router.get("/", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
):
    async with get_db() as db:
        db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        rows = await db.execute_fetchall(
            """
            SELECT
                p.id,
                p.url,
                p.title,
                p.content,
                p.rank_score,
                fts.rank AS fts_rank
            FROM pages_fts fts
            JOIN pages p ON p.id = fts.rowid
            WHERE pages_fts MATCH ?
            ORDER BY (p.rank_score * 0.6 + (-fts.rank) * 0.4) DESC
            LIMIT ?
            """,
            (q, limit),
        )

    results = [
        SearchResult(
            id=r["id"],
            url=r["url"],
            title=r["title"] or r["url"],
            snippet=make_snippet(r["content"] or "", q),
            rank_score=r["rank_score"],
            fts_score=float(-r["fts_rank"]),
            combined_score=r["rank_score"] * 0.6 + float(-r["fts_rank"]) * 0.4,
        )
        for r in rows
    ]

    return SearchResponse(query=q, total=len(results), results=results)