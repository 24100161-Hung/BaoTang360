"""
Gợi ý scene tương tự dựa trên TF-IDF + cosine similarity.
"""
from __future__ import annotations
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import text
from .analytics import _engine

_cache: dict = {}


def _load_scenes() -> pd.DataFrame:
    query = text("""
        SELECT s.id, s.title, s.slug, s.description, c.name AS category
        FROM scenes s
        LEFT JOIN categories c ON c.id = (
            SELECT category_id FROM products WHERE id = s.id LIMIT 1
        )
        WHERE s.is_published = TRUE
    """)
    try:
        df = pd.read_sql(query, _engine)
    except Exception:
        # Nếu query phức tạp lỗi, dùng query đơn giản
        df = pd.read_sql(
            text("SELECT id, title, slug, description FROM scenes WHERE is_published = TRUE"),
            _engine,
        )
        df["category"] = ""

    df["text"] = (
        df["title"].fillna("") + " "
        + df["description"].fillna("") + " "
        + df["category"].fillna("")
    )
    return df


def _get_matrix():
    if "M" not in _cache:
        df = _load_scenes()
        vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1)
        X = vec.fit_transform(df["text"])
        _cache["df"] = df
        _cache["M"] = cosine_similarity(X)
    return _cache["df"], _cache["M"]


def recommend_scenes(scene_id: int, k: int = 5) -> list[dict]:
    df, M = _get_matrix()
    if scene_id not in set(df["id"]):
        return []
    idx = df.index[df["id"] == scene_id][0]
    scores = pd.Series(M[idx], index=df.index).drop(idx)
    top = scores.sort_values(ascending=False).head(k)

    return [
        {
            "scene_id": int(df.at[i, "id"]),
            "title": df.at[i, "title"],
            "slug": df.at[i, "slug"],
            "similarity": round(float(s), 4),
        }
        for i, s in top.items()
    ]


def refresh_cache():
    _cache.clear()
