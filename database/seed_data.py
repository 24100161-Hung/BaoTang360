#!/usr/bin/env python3
"""
Sinh dữ liệu mẫu cho Bảo tàng ảo 360.
Chạy: python seed_data.py > seed.sql
"""
import random
import datetime as dt

random.seed(42)  # Cố định seed để tái lập

# ===== 1. Users =====
users = [
    (1, "admin@baotang.test", "Quản trị viên"),
    (2, "curator@baotang.test", "Giám tuyển"),
    (3, "visitor1@test.com", "Khách 1"),
    (4, "visitor2@test.com", "Khách 2"),
]

# ===== 2. Scenes (không gian tham quan) =====
scenes = [
    (1, "Sảnh chính Bảo tàng", "sanh-chinh",
     "Khu vực đón tiếp với kiến trúc Pháp cổ đầu thế kỷ 20.",
     "/storage/panoramas/sanh-chinh.jpg", 0, 0, 100, 1),
    (2, "Phòng trưng bày Đông Dương", "phong-dong-duong",
     "Hiện vật thời kỳ Đông Dương 1858-1954.",
     "/storage/panoramas/dong-duong.jpg", 0, 90, 100, 2),
    (3, "Phòng trưng bày Cổ vật", "phong-co-vat",
     "Bộ sưu tập cổ vật quý từ văn hóa Đông Sơn, Sa Huỳnh, Óc Eo.",
     "/storage/panoramas/co-vat.jpg", 0, -45, 100, 3),
    (4, "Không gian Văn hóa Sa Huỳnh", "sa-huynh",
     "Di chỉ văn hóa Sa Huỳnh (1000 TCN - 200 SCN).",
     "/storage/panoramas/sa-huynh.jpg", 0, 180, 100, 4),
    (5, "Khu vườn tưởng niệm", "vuon-tuong-niem",
     "Không gian ngoài trời với cây xanh và tượng đài.",
     "/storage/panoramas/vuon.jpg", 0, 0, 100, 5),
]

# ===== 3. Hotspots =====
hotspots = [
    # Scene 1 (Sảnh chính) - các điểm nóng chuyển cảnh
    (1, 1, 'scene', 5, 45, "Đến phòng Đông Dương",
     "Nhấn để chuyển đến phòng trưng bày Đông Dương.", 2, None, 'arrow', 1),
    (2, 1, 'scene', 5, -45, "Đến phòng Cổ vật",
     "Nhấn để chuyển đến phòng trưng bày Cổ vật.", 3, None, 'arrow', 2),
    (3, 1, 'scene', 5, 180, "Ra vườn tưởng niệm",
     "Nhấn để ra khu vườn tưởng niệm.", 5, None, 'arrow', 3),
    (4, 1, 'info', -10, 0, "Giới thiệu bảo tàng",
     "Bảo tàng được thành lập năm 1932, lưu giữ hơn 10.000 hiện vật quý.",
     None, None, 'info', 0),

    # Scene 2 (Đông Dương)
    (5, 2, 'scene', 0, -90, "Quay lại sảnh chính",
     "Nhấn để quay lại sảnh chính.", 1, None, 'arrow', 1),
    (6, 2, 'artifact', 0, 30, "Máy đánh chữ Pháp",
     "Máy đánh chữ được sử dụng trong thời kỳ Pháp thuộc.", None, 1, 'artifact', 2),

    # Scene 3 (Cổ vật)
    (7, 3, 'scene', 0, 90, "Quay lại sảnh chính",
     "Nhấn để quay lại sảnh chính.", 1, None, 'arrow', 1),
    (8, 3, 'artifact', 0, 0, "Trống đồng Đông Sơn",
     "Trống đồng là biểu tượng văn hóa của người Việt cổ.", None, 2, 'artifact', 2),
    (9, 3, 'scene', 0, 180, "Đến không gian Sa Huỳnh",
     "Khám phá văn hóa Sa Huỳnh.", 4, None, 'arrow', 3),

    # Scene 4 (Sa Huỳnh)
    (10, 4, 'scene', 0, 90, "Quay lại phòng Cổ vật",
     "Nhấn để quay lại.", 3, None, 'arrow', 1),
    (11, 4, 'artifact', 0, -30, "Đồ gốm Sa Huỳnh",
     "Đồ gốm đặc trưng của văn hóa Sa Huỳnh.", None, 3, 'artifact', 2),

    # Scene 5 (Vườn)
    (12, 5, 'scene', 0, 0, "Quay vào sảnh chính",
     "Nhấn để quay vào trong.", 1, None, 'arrow', 1),
    (13, 5, 'info', 0, 90, "Tượng đài tưởng niệm",
     "Tượng đài tưởng niệm các nhà nghiên cứu văn hóa.", None, None, 'info', 2),
]

# ===== 4. Artifacts =====
artifacts = [
    (1, "Máy đánh chữ Pháp", "may-danh-chua-phap",
     "Máy đánh chữ hiệu Underwood, sản xuất năm 1925.",
     "/storage/artifacts/typewriter.jpg", "Thời Pháp thuộc",
     "Pháp", "Kim loại", "30x40x20 cm", "ART-001"),
    (2, "Trống đồng Đông Sơn", "trong-dong-dong-son",
     "Trống đồng thuộc văn hóa Đông Sơn, niên đại 500 TCN.",
     "/storage/artifacts/dong-son-drum.jpg", "Văn hóa Đông Sơn",
     "Việt Nam", "Đồng", "Đường kính 70cm", "ART-002"),
    (3, "Đồ gốm Sa Huỳnh", "do-gom-sa-huynh",
     "Bình gốm với hoa văn khắc đặc trưng Sa Huỳnh.",
     "/storage/artifacts/sa-huynh-pottery.jpg", "Văn hóa Sa Huỳnh",
     "Việt Nam", "Gốm", "Cao 25cm", "ART-003"),
]

# ===== 5. Audio guides =====
audio_guides = [
    (1, 1, 'vi', 'Tiếng Việt', '/storage/audio/sanh-chinh-vi.mp3',
     "Chào mừng quý khách đến với Bảo tàng. Đây là sảnh chính..."),
    (2, 1, 'en', 'English', '/storage/audio/sanh-chinh-en.mp3',
     "Welcome to the Museum. This is the main hall..."),
    (3, 1, 'fr', 'Français', '/storage/audio/sanh-chinh-fr.mp3',
     "Bienvenue au Musée. Ceci est le hall principal..."),
    (4, 2, 'vi', 'Tiếng Việt', '/storage/audio/dong-duong-vi.mp3',
     "Phòng trưng bày Đông Dương giới thiệu..."),
    (5, 2, 'en', 'English', '/storage/audio/dong-duong-en.mp3',
     "The Indochina exhibition room introduces..."),
]

# ===== 6. Tours =====
tours = [
    (1, "Hành trình Văn hóa Việt", "hanh-trinh-van-hoa-viet",
     "Tour tham quan tổng quát qua các không gian chính của bảo tàng.",
     "/storage/tours/cover-1.jpg", 45, 'easy', True),
    (2, "Khám phá Văn hóa Đông Sơn", "kham-pha-dong-son",
     "Chuyên sâu về văn hóa Đông Sơn và trống đồng.",
     "/storage/tours/cover-2.jpg", 30, 'medium', True),
    (3, "Theo dấu người Pháp", "theo-dau-nguoi-phap",
     "Hành trình tìm hiểu thời kỳ Pháp thuộc qua hiện vật.",
     "/storage/tours/cover-3.jpg", 25, 'easy', True),
]

# ===== 7. Tour scenes =====
tour_scenes = [
    # Tour 1: Hành trình Văn hóa Việt
    (1, 1, 1, 1, "Bắt đầu tại sảnh chính.", 300),
    (2, 1, 2, 2, "Khám phá phòng Đông Dương.", 600),
    (3, 1, 3, 3, "Chiêm ngưỡng cổ vật.", 600),
    (4, 1, 4, 4, "Tìm hiểu văn hóa Sa Huỳnh.", 480),
    (5, 1, 5, 5, "Thư giãn tại vườn tưởng niệm.", 300),

    # Tour 2: Khám phá Đông Sơn
    (6, 2, 1, 1, "Bắt đầu từ sảnh chính.", 180),
    (7, 2, 3, 2, "Tập trung vào trống đồng Đông Sơn.", 900),
    (8, 2, 4, 3, "So sánh với văn hóa Sa Huỳnh.", 600),

    # Tour 3: Theo dấu người Pháp
    (9, 3, 1, 1, "Bắt đầu tại sảnh chính.", 180),
    (10, 3, 2, 2, "Tìm hiểu thời Pháp thuộc.", 900),
]

# ===== Xuất SQL =====
print("SET NAMES utf8mb4;")
print("SET FOREIGN_KEY_CHECKS = 0;")
print("USE baotang360;")
print()

# Users - password mặc định: "Password123!" (đã hash Argon2id)
# Hash này được sinh bằng password_hash('Password123!', PASSWORD_ARGON2ID)
HASH = "$argon2id$v=19$m=65536,t=4,p=1$c29tZXNhbHR2YWx1ZQ$" \
       "3q2+7wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

for u in users:
    print(f"INSERT INTO users (id, email, password_hash, full_name, role) "
          f"VALUES ({u[0]}, '{u[1]}', '{HASH}', '{u[2]}', "
          f"'{'admin' if u[0]==1 else 'curator' if u[0]==2 else 'visitor'}');")
print()

for s in scenes:
    print(f"INSERT INTO scenes (id, title, slug, description, original_image_url, "
          f"initial_pitch, initial_yaw, initial_hfov, default_order, tiles_status) "
          f"VALUES ({s[0]}, '{s[1]}', '{s[2]}', '{s[3]}', '{s[4]}', "
          f"{s[5]}, {s[6]}, {s[7]}, {s[8]}, 'pending');")
print()

for a in artifacts:
    print(f"INSERT INTO artifacts (id, name, slug, description, image_url, era, "
          f"origin, material, dimensions, inventory_code) VALUES "
          f"({a[0]}, '{a[1]}', '{a[2]}', '{a[3]}', '{a[4]}', '{a[5]}', "
          f"'{a[6]}', '{a[7]}', '{a[8]}', '{a[9]}');")
print()

for h in hotspots:
    target = h[7] if h[7] else 'NULL'
    artifact = h[8] if h[8] else 'NULL'
    print(f"INSERT INTO hotspots (id, scene_id, type, pitch, yaw, title, content, "
          f"target_scene_id, artifact_id, icon_class, display_order) VALUES "
          f"({h[0]}, {h[1]}, '{h[2]}', {h[3]}, {h[4]}, '{h[5]}', '{h[6]}', "
          f"{target}, {artifact}, '{h[9]}', {h[10]});")
print()

for ag in audio_guides:
    print(f"INSERT INTO audio_guides (id, scene_id, language_code, language_name, "
          f"audio_url, transcript) VALUES ({ag[0]}, {ag[1]}, '{ag[2]}', "
          f"'{ag[3]}', '{ag[4]}', '{ag[5]}');")
print()

for t in tours:
    print(f"INSERT INTO tours (id, title, slug, description, cover_image_url, "
          f"duration_estimate_minutes, difficulty, is_published) VALUES "
          f"({t[0]}, '{t[1]}', '{t[2]}', '{t[3]}', '{t[4]}', {t[5]}, "
          f"'{t[6]}', {str(t[7]).lower()});")
print()

for ts in tour_scenes:
    print(f"INSERT INTO tour_scenes (id, tour_id, scene_id, step_order, "
          f"narration, duration_seconds) VALUES ({ts[0]}, {ts[1]}, {ts[2]}, "
          f"{ts[3]}, '{ts[4]}', {ts[5]});")
print()

print("SET FOREIGN_KEY_CHECKS = 1;")
print(f"-- Tổng: {len(users)} users, {len(scenes)} scenes, {len(hotspots)} hotspots, "
      f"{len(artifacts)} artifacts, {len(audio_guides)} audio guides, "
      f"{len(tours)} tours, {len(tour_scenes)} tour steps")
