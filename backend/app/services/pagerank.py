import numpy as np


def compute_pagerank(
    n: int,
    edges: list[tuple[int, int]],
    d: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 200,
) -> tuple[np.ndarray, list[float]]:
    """
    Power-iteration PageRank.
    Returns rank vector + convergence history (L2 delta per iteration).
    """
    if n == 0:
        return np.array([]), []

    M = np.zeros((n, n))
    for src, tgt in edges:
        if 0 <= src < n and 0 <= tgt < n:
            M[tgt][src] += 1.0

    col_sums = M.sum(axis=0)
    dangling = col_sums == 0
    col_sums[dangling] = 1.0
    M = M / col_sums
    M[:, dangling] = 1.0 / n

    teleport = np.ones(n) / n
    rank = np.ones(n) / n
    convergence = []

    for _ in range(max_iter):
        new_rank = d * (M @ rank) + (1 - d) * teleport
        delta = float(np.linalg.norm(new_rank - rank))
        convergence.append(delta)
        rank = new_rank
        if delta < tol:
            break

    return rank, convergence


def rank_to_scores(rank: np.ndarray, page_ids: list[int]) -> dict[int, float]:
    return {pid: float(rank[i]) for i, pid in enumerate(page_ids)}