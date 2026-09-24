"""
FastAPI service - Data Service cho Bảo tàng ảo 360°.
"""
from fastapi import FastAPI, Header, HTTPException, Query
from . import analytics, recommender
from .config import config

app = FastAPI(
    title="Bảo tàng ảo - Data Service",
    description="Phân tích hành vi tham quan và gợi ý",
    version="1.0.0",
)


def verify_token(x_service_token: str | None = Header(default=None)):
    """Kiểm tra token nội bộ."""
    if config.PY_SERVICE_TOKEN and x_service_token != config.PY_SERVICE_TOKEN:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")


@app.get("/healthz")
def health():
    """Endpoint kiểm tra tình trạng."""
    return {"status": "ok", "service": "python-data-service"}


@app.get("/analytics/drop-off")
def api_drop_off(
    min_sessions: int = Query(3, ge=1),
    x_service_token: str | None = Header(default=None),
):
    """Phân tích điểm bỏ dở."""
    verify_token(x_service_token)
    return {"data": analytics.analyze_drop_off(min_sessions)}


@app.get("/analytics/tour-flow")
def api_tour_flow(
    session_id: str | None = Query(None),
    x_service_token: str | None = Header(default=None),
):
    """Luồng tham quan."""
    verify_token(x_service_token)
    return {"data": analytics.get_tour_flow(session_id)}


@app.get("/analytics/scene-heatmap/{scene_id}")
def api_scene_heatmap(
    scene_id: int,
    x_service_token: str | None = Header(default=None),
):
    """Heatmap hotspot."""
    verify_token(x_service_token)
    return {"data": analytics.get_scene_heatmap(scene_id)}


@app.get("/analytics/visitor-stats")
def api_visitor_stats(x_service_token: str | None = Header(default=None)):
    """Thống kê tổng quan."""
    verify_token(x_service_token)
    return {"data": analytics.get_visitor_stats()}


@app.get("/analytics/top-destinations")
def api_top_destinations(
    limit: int = Query(10, ge=1, le=50),
    x_service_token: str | None = Header(default=None),
):
    """Top điểm đến."""
    verify_token(x_service_token)
    return {"data": analytics.get_top_destinations(limit)}


@app.get("/recommend/scenes/{scene_id}")
def api_recommend(
    scene_id: int,
    k: int = Query(5, ge=1, le=20),
    x_service_token: str | None = Header(default=None),
):
    """Gợi ý scenes tương tự."""
    verify_token(x_service_token)
    return {"data": recommender.recommend_scenes(scene_id, k)}


@app.post("/cache/refresh")
def api_refresh(x_service_token: str | None = Header(default=None)):
    """Refresh cache."""
    verify_token(x_service_token)
    recommender.refresh_cache()
    return {"status": "refreshed"}
