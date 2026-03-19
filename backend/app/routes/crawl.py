from fastapi import APIRouter
from app.models.schemas import CrawlRequest, CrawlStatus
from app.services.crawler import crawl
from app.services.pagerank import compute_pagerank, rank_to_scores
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=CrawlStatus)
async def start_crawl(req: CrawlRequest):
    pages, links = await crawl(
        seed_url=str(req.seed_url),
        max_depth=req.max_depth,
        max_pages=req.max_pages,
    )

    async with get_db() as db:
        url_to_id: dict[str, int] = {}
        for page in pages:
            cursor = await db.execute(
                """
                INSERT INTO pages (url, title, content)
                VALUES (?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    title   = excluded.title,
                    content = excluded.content
                RETURNING id
                """,
                (page["url"], page["title"], page["content"]),
            )
            row = await cursor.fetchone()
            url_to_id[page["url"]] = row[0]

        edge_pairs: list[tuple[int, int]] = []
        for src_url, tgt_url in links:
            src_id = url_to_id.get(src_url)
            tgt_id = url_to_id.get(tgt_url)
            if src_id and tgt_id:
                await db.execute(
                    "INSERT OR IGNORE INTO links (source_id, target_id) VALUES (?, ?)",
                    (src_id, tgt_id),
                )
                edge_pairs.append((src_id, tgt_id))

        await db.commit()

        page_ids = list(url_to_id.values())
        id_to_idx = {pid: i for i, pid in enumerate(page_ids)}
        indexed_edges = [
            (id_to_idx[s], id_to_idx[t])
            for s, t in edge_pairs
            if s in id_to_idx and t in id_to_idx
        ]
        rank_vector, _ = compute_pagerank(len(page_ids), indexed_edges)
        scores = rank_to_scores(rank_vector, page_ids)

        for pid, score in scores.items():
            await db.execute(
                "UPDATE pages SET rank_score = ? WHERE id = ?", (score, pid)
            )
        await db.commit()

    return CrawlStatus(
        pages_crawled=len(pages),
        links_found=len(links),
        pagerank_computed=True,
    )