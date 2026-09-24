"""
Phân tích hành vi tham quan từ bảng tour_logs.
"""
from __future__ import annotations
import pandas as pd
from sqlalchemy import create_engine, text
from .config import config

_engine = create_engine(config.dsn, pool_pre_ping=True, pool_recycle=1800)


def analyze_drop_off(min_sessions: int = 3) -> list[dict]:
    """
    Phát hiện điểm bỏ dở:
    - Scene có tỷ lệ thoát cao (ít chuyển scene tiếp)
    - Scene có thời gian xem trung bình thấp
    """
    query = text("""
        SELECT
            s.id AS scene_id,
            s.title AS scene_title,
            COUNT(DISTINCT l.session_id) AS unique_sessions,
            COUNT(CASE WHEN l.action = 'scene_change' THEN 1 END) AS scene_changes,
            COUNT(CASE WHEN l.action = 'view' THEN 1 END) AS views,
            COUNT(CASE WHEN l.action = 'hotspot_click' THEN 1 END) AS hotspot_clicks,
            COALESCE(AVG(CASE WHEN l.duration_seconds > 0 THEN l.duration_seconds END), 0) AS avg_duration
        FROM scenes s
        LEFT JOIN tour_logs l ON l.scene_id = s.id
        WHERE l.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY s.id, s.title
        HAVING unique_sessions >= :min_sessions
        ORDER BY unique_sessions DESC
    """)

    df = pd.read_sql(query, _engine, params={"min_sessions": min_sessions})

    if df.empty:
        return []

    df["exit_rate"] = (
        1 - (df["scene_changes"] / df["views"].clip(lower=1))
    ).round(3)

    engagement = (
        (df["hotspot_clicks"] / df["views"].clip(lower=1)).clip(0, 1) * 0.4
        + (df["avg_duration"] / 300).clip(0, 1) * 0.6
    )
    df["engagement_score"] = engagement.round(3)

    df["is_drop_off"] = (df["exit_rate"] > 0.7) & (df["engagement_score"] < 0.4)

    return df.fillna(0).to_dict(orient="records")


def get_tour_flow(session_id: str | None = None) -> list[dict]:
    """Lấy luồng tham quan của một session."""
    if session_id:
        query = text("""
            SELECT l.id, l.session_id, l.scene_id, s.title AS scene_title,
                   l.action, l.hotspot_id, h.title AS hotspot_title,
                   l.duration_seconds, l.created_at
            FROM tour_logs l
            JOIN scenes s ON s.id = l.scene_id
            LEFT JOIN hotspots h ON h.id = l.hotspot_id
            WHERE l.session_id = :sid
            ORDER BY l.created_at ASC
        """)
        params = {"sid": session_id}
    else:
        query = text("""
            SELECT l.id, l.session_id, l.scene_id, s.title AS scene_title,
                   l.action, l.hotspot_id, h.title AS hotspot_title,
                   l.duration_seconds, l.created_at
            FROM tour_logs l
            JOIN scenes s ON s.id = l.scene_id
            LEFT JOIN hotspots h ON h.id = l.hotspot_id
            WHERE l.session_id IN (
                SELECT session_id FROM tour_logs
                GROUP BY session_id
                ORDER BY MAX(created_at) DESC
                LIMIT 20
            )
            ORDER BY l.session_id, l.created_at ASC
        """)
        params = {}

    df = pd.read_sql(query, _engine, params=params)
    return df.to_dict(orient="records")


def get_scene_heatmap(scene_id: int) -> list[dict]:
    """Lấy tần suất click hotspot trên một scene."""
    query = text("""
        SELECT
            h.id AS hotspot_id,
            h.title AS hotspot_title,
            h.type AS hotspot_type,
            h.pitch, h.yaw,
            COUNT(l.id) AS click_count
        FROM hotspots h
        LEFT JOIN tour_logs l ON l.hotspot_id = h.id AND l.action = 'hotspot_click'
        WHERE h.scene_id = :scene_id
        GROUP BY h.id, h.title, h.type, h.pitch, h.yaw
        ORDER BY click_count DESC
    """)

    df = pd.read_sql(query, _engine, params={"scene_id": scene_id})
    return df.to_dict(orient="records")


def get_visitor_stats() -> dict:
    """Thống kê tổng quan về người tham quan."""
    query = text("""
        SELECT
            COUNT(DISTINCT session_id) AS total_sessions,
            COUNT(DISTINCT CASE WHEN user_id IS NOT NULL THEN user_id END) AS logged_users,
            COUNT(*) AS total_actions,
            COALESCE(AVG(duration_seconds), 0) AS avg_duration,
            COUNT(CASE WHEN action = 'hotspot_click' THEN 1 END) AS total_hotspot_clicks,
            COUNT(CASE WHEN action = 'audio_play' THEN 1 END) AS total_audio_plays
        FROM tour_logs
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)

    try:
        with _engine.connect() as conn:
            result = conn.execute(query).mappings().first()
        if not result:
            return {}
        # Chuyển Decimal về float, None về 0
        return {k: (float(v) if v is not None else 0) for k, v in result.items()}
    except Exception as e:
        print(f"Error in get_visitor_stats: {e}")
        return {}


def get_top_destinations(limit: int = 10) -> list[dict]:
    """Top điểm đến được tham quan nhiều nhất."""
    query = text("""
        SELECT
            s.id AS scene_id,
            s.title AS scene_title,
            COUNT(DISTINCT l.session_id) AS visits,
            COALESCE(AVG(l.duration_seconds), 0) AS avg_duration
        FROM scenes s
        JOIN tour_logs l ON l.scene_id = s.id AND l.action = 'view'
        WHERE l.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY s.id, s.title
        ORDER BY visits DESC
        LIMIT :lim
    """)

    try:
        with _engine.connect() as conn:
            result = conn.execute(query, {"lim": limit}).mappings().all()
        return [
            {
                "scene_id": int(r["scene_id"]),
                "scene_title": r["scene_title"],
                "visits": int(r["visits"]),
                "avg_duration": float(r["avg_duration"] or 0),
            }
            for r in result
        ]
    except Exception as e:
        print(f"Error in get_top_destinations: {e}")
        return []
