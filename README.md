# 🔍 lav-oogle

a mini search engine built for fun after covering PageRank in lectures. crawls a bounded web graph, indexes pages into SQLite with FTS5, and ranks
results by a hybrid of text relevance and PageRank computed via NumPy power iteration.

---

## stack

| layer    | tech                           |
|----------|--------------------------------|
| backend  | FastAPI, SQLite (FTS5), NumPy  |
| crawler  | httpx, BeautifulSoup4          |
| frontend | React + Vite, Recharts         |
| env      | Python venv, WSL               |
