import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


async def crawl(
    seed_url: str,
    max_depth: int = 2,
    max_pages: int = 50,
    timeout: float = 10.0,
) -> tuple[list[dict], list[tuple[str, str]]]:
    seed_domain = urlparse(seed_url).netloc
    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(seed_url, 0)])
    pages: list[dict] = []
    links: list[tuple[str, str]] = []

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": "Lav-oogle/0.1 (+educational-crawler)"},
    ) as client:
        while queue and len(pages) < max_pages:
            url, depth = queue.popleft()
            if url in visited:
                continue
            visited.add(url)

            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                if "text/html" not in resp.headers.get("content-type", ""):
                    continue
            except Exception:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title else url
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            content = " ".join(soup.get_text(separator=" ").split())[:5000]
            pages.append({"url": url, "title": title, "content": content})

            if depth < max_depth:
                for a_tag in soup.find_all("a", href=True):
                    absolute = urljoin(url, a_tag["href"])
                    parsed = urlparse(absolute)
                    if (
                        parsed.scheme in ("http", "https")
                        and parsed.netloc == seed_domain
                        and absolute not in visited
                    ):
                        links.append((url, absolute))
                        queue.append((absolute, depth + 1))

    return pages, links