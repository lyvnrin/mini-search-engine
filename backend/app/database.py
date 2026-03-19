import aiosqlite
import os

DB_PATH = os.getenv("DATABASE_URL", "./lavoogle.db")

CREATE_PAGES = """
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT    UNIQUE NOT NULL,
    title       TEXT,
    content     TEXT,
    rank_score  REAL    DEFAULT 0.0,
    crawled_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_LINKS = """
CREATE TABLE IF NOT EXISTS links (
    source_id   INTEGER NOT NULL REFERENCES pages(id),
    target_id   INTEGER NOT NULL REFERENCES pages(id),
    PRIMARY KEY (source_id, target_id)
);
"""

CREATE_FTS = """
CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts
USING fts5(title, content, content='pages', content_rowid='id');
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA foreign_keys=ON;")
        await db.execute(CREATE_PAGES)
        await db.execute(CREATE_LINKS)
        await db.execute(CREATE_FTS)
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN
                INSERT INTO pages_fts(rowid, title, content)
                VALUES (new.id, new.title, new.content);
            END
        """)
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS pages_au AFTER UPDATE ON pages BEGIN
                INSERT INTO pages_fts(pages_fts, rowid, title, content)
                VALUES ('delete', old.id, old.title, old.content);
                INSERT INTO pages_fts(rowid, title, content)
                VALUES (new.id, new.title, new.content);
            END
        """)
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS pages_ad AFTER DELETE ON pages BEGIN
                INSERT INTO pages_fts(pages_fts, rowid, title, content)
                VALUES ('delete', old.id, old.title, old.content);
            END
        """)
        await db.commit()

def get_db():
    return aiosqlite.connect(DB_PATH)