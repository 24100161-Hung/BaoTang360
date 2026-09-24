"""
ETL: Làm sạch dữ liệu điểm đến.
"""
from __future__ import annotations
import os
import re
import unicodedata
import pandas as pd
from sqlalchemy import create_engine, text
from .config import config

_engine = create_engine(config.dsn, pool_pre_ping=True)


def bo_dau(s: str) -> str:
    """Bỏ dấu tiếng Việt để so khớp và sinh slug."""
    nfkd = unicodedata.normalize("NFKD", str(s))
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def slug_hoa(s: str) -> str:
    s = bo_dau(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def lam_sach(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu."""
    n0 = len(df)

    # Chuẩn hóa tên cột
    df.columns = [slug_hoa(c).replace("-", "_") for c in df.columns]

    # Loại bản ghi thiếu trường bắt buộc
    if "name" in df.columns and "province" in df.columns:
        df = df.dropna(subset=["name", "province"])

    # Chuẩn hóa tọa độ
    for col in ("lat", "lng", "long"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Lọc tọa độ trong phạm vi Việt Nam
    if "lat" in df.columns and "lng" in df.columns:
        df = df[
            df["lat"].between(8.0, 24.0)
            & df["lng"].between(102.0, 110.0)
        ]

    # Khử trùng lặp
    if "name" in df.columns:
        df["slug"] = df["name"].apply(slug_hoa)
        df = df.drop_duplicates(subset=["slug"], keep="first")

    print(f"Làm sạch: {n0} → {len(df)} bản ghi")
    return df


def main():
    """Chạy ETL từ file CSV."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.input, encoding="utf-8")
    df = lam_sach(df)

    if args.dry_run:
        print(df.head())
        return

    print(f"Đã xử lý {len(df)} bản ghi")


if __name__ == "__main__":
    main()
