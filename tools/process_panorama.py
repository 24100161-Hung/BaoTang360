#!/usr/bin/env python3
"""
Xử lý ảnh 360° equirectangular thành tiles đa phân giải.
Sử dụng generate.py của Pannellum (cần Hugin/nona).

Cách dùng:
    python3 process_panorama.py <input.jpg> <output_dir> [--tile-size 512] [--depth 3]
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def generate_tiles(input_image: str, output_dir: str,
                   tile_size: int = 512,
                   depth: int = 3,
                   quality: int = 85) -> dict:
    """
    Tạo tiles đa phân giải từ ảnh equirectangular.
    Trả về dict cấu hình multires cho Pannellum.
    """
    if not os.path.isfile(input_image):
        raise FileNotFoundError(f"Không tìm thấy file: {input_image}")

    os.makedirs(output_dir, exist_ok=True)

    # Đường dẫn đến generate.py (cùng thư mục)
    script_dir = Path(__file__).parent
    generate_script = script_dir / "generate.py"

    if not generate_script.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {generate_script}. "
            "Tải từ https://raw.githubusercontent.com/mpetroff/pannellum/master/utils/multires/generate.py"
        )

    cmd = [
        sys.executable, str(generate_script),
        str(input_image),
        "--output", str(output_dir),
        "--tilesize", str(tile_size),
        "--quality", str(quality),
        "--depth", str(depth),
    ]

    print(f"→ Đang xử lý: {input_image}")
    print(f"  Output: {output_dir}")
    print(f"  Tile size: {tile_size}px, Depth: {depth}, Quality: {quality}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"LỖI: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"generate.py thất bại: {result.stderr}")

    # Đọc config.json do generate.py tạo ra
    config_path = Path(output_dir) / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        print(f"✓ Đã tạo tiles thành công")
        return config

    # Nếu không có config.json, tự sinh cấu hình
    return {
        "multiRes": {
            "path": f"/{output_dir}/%l/%s%y_%x",
            "fallbackPath": f"/{output_dir}/fallback/%s",
            "extension": "jpg",
            "tileResolution": tile_size,
            "maxLevel": depth,
            "cubeResolution": 4096,
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Xử lý ảnh 360 thành tiles")
    parser.add_argument("input", help="Đường dẫn ảnh equirectangular")
    parser.add_argument("output", help="Thư mục output cho tiles")
    parser.add_argument("--tile-size", type=int, default=512, help="Kích thước mỗi tile")
    parser.add_argument("--depth", type=int, default=3, help="Số cấp độ zoom")
    parser.add_argument("--quality", type=int, default=85, help="Chất lượng JPEG (1-100)")

    args = parser.parse_args()

    try:
        config = generate_tiles(
            args.input,
            args.output,
            tile_size=args.tile_size,
            depth=args.depth,
            quality=args.quality,
        )
        print("\n=== Cấu hình multires ===")
        print(json.dumps(config, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"LỖI: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
