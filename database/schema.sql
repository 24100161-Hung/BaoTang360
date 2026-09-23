-- =====================================================================
-- Bảo tàng ảo 360° - Schema MySQL 8.0
-- Charset: utf8mb4 để hỗ trợ tiếng Việt và emoji
-- =====================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================================
-- 1. NGƯỜI DÙNG VÀ PHÂN QUYỀN
-- =====================================================================
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(160) NOT NULL,
    role ENUM('admin','curator','visitor') NOT NULL DEFAULT 'visitor',
    status ENUM('active','locked') NOT NULL DEFAULT 'active',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_role_status (role, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 2. KHÔNG GIAN THAM QUAN (SCENE) - Ảnh 360°
-- =====================================================================
CREATE TABLE scenes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(220) NOT NULL UNIQUE,
    description TEXT NULL,

    -- Ảnh equirectangular gốc (đã upload)
    original_image_url VARCHAR(500) NOT NULL,
    -- Đường dẫn thư mục chứa tiles đa phân giải (sau khi xử lý)
    tiles_path VARCHAR(500) NULL,
    -- Trạng thái xử lý tiles: pending / processing / done / failed
    tiles_status ENUM('pending','processing','done','failed') DEFAULT 'pending',

    -- Điểm nhìn mặc định khi load scene (tọa độ cầu)
    initial_pitch DECIMAL(8,4) DEFAULT 0,
    initial_yaw DECIMAL(8,4) DEFAULT 0,
    initial_hfov DECIMAL(8,4) DEFAULT 100,

    -- Thứ tự trong tour mặc định
    default_order INT DEFAULT 0,

    -- Metadata
    is_published BOOLEAN DEFAULT TRUE,
    created_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_scenes_slug (slug),
    INDEX idx_scenes_order (default_order),
    INDEX idx_scenes_status (tiles_status),
    CONSTRAINT fk_scenes_creator FOREIGN KEY (created_by)
        REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 3. ĐIỂM NÓNG (HOTSPOT) - Tọa độ cầu
-- =====================================================================
CREATE TABLE hotspots (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    scene_id BIGINT UNSIGNED NOT NULL,

    -- Loại: info (thông tin), scene (chuyển cảnh), artifact (hiện vật)
    type ENUM('info','scene','artifact') NOT NULL DEFAULT 'info',

    -- Tọa độ cầu: pitch (dọc, -90..90), yaw (ngang, -180..180)
    pitch DECIMAL(8,4) NOT NULL,
    yaw DECIMAL(8,4) NOT NULL,

    title VARCHAR(200) NOT NULL,
    content TEXT NULL,

    -- Nếu type='scene': trỏ đến scene đích
    target_scene_id BIGINT UNSIGNED NULL,
    -- Nếu type='artifact': trỏ đến hiện vật
    artifact_id BIGINT UNSIGNED NULL,

    -- Icon: 'info', 'arrow', 'artifact', hoặc custom CSS class
    icon_class VARCHAR(80) DEFAULT 'hotspot-info',

    -- Thứ tự hiển thị (nếu có nhiều hotspot cùng vị trí)
    display_order INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_hs_scene FOREIGN KEY (scene_id)
        REFERENCES scenes(id) ON DELETE CASCADE,
    CONSTRAINT fk_hs_target FOREIGN KEY (target_scene_id)
        REFERENCES scenes(id) ON DELETE SET NULL,
    INDEX idx_hs_scene (scene_id),
    INDEX idx_hs_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 4. HIỆN VẬT (ARTIFACT)
-- =====================================================================
CREATE TABLE artifacts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    slug VARCHAR(270) NOT NULL UNIQUE,
    description TEXT NULL,
    image_url VARCHAR(500) NULL,
    era VARCHAR(100) NULL,        -- Thời kỳ
    origin VARCHAR(200) NULL,     -- Nguồn gốc
    material VARCHAR(150) NULL,   -- Chất liệu
    dimensions VARCHAR(150) NULL, -- Kích thước
    inventory_code VARCHAR(80) NULL, -- Mã số hiện vật
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_artifacts_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Thêm FK cho hotspots.artifact_id sau khi artifacts đã tạo
ALTER TABLE hotspots
    ADD CONSTRAINT fk_hs_artifact FOREIGN KEY (artifact_id)
        REFERENCES artifacts(id) ON DELETE SET NULL;

-- =====================================================================
-- 5. THUYẾT MINH ÂM THANH ĐA NGỮ
-- =====================================================================
CREATE TABLE audio_guides (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    scene_id BIGINT UNSIGNED NOT NULL,
    language_code VARCHAR(10) NOT NULL,     -- vi, en, fr, ja, zh, ko
    language_name VARCHAR(50) NOT NULL,     -- Tiếng Việt, English, ...
    audio_url VARCHAR(500) NOT NULL,
    transcript TEXT NULL,                    -- Bản ghi lời thuyết minh
    duration_seconds INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ag_scene FOREIGN KEY (scene_id)
        REFERENCES scenes(id) ON DELETE CASCADE,
    UNIQUE KEY uq_ag_scene_lang (scene_id, language_code),
    INDEX idx_ag_lang (language_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 6. TOUR THEO CHỦ ĐỀ
-- =====================================================================
CREATE TABLE tours (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    slug VARCHAR(270) NOT NULL UNIQUE,
    description TEXT NULL,
    cover_image_url VARCHAR(500) NULL,
    duration_estimate_minutes INT DEFAULT 30,
    difficulty ENUM('easy','medium','hard') DEFAULT 'easy',
    is_published BOOLEAN DEFAULT FALSE,
    created_by BIGINT UNSIGNED NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tours_creator FOREIGN KEY (created_by)
        REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_tours_slug (slug),
    INDEX idx_tours_published (is_published)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 7. CÁC SCENE TRONG TOUR (có thứ tự)
-- =====================================================================
CREATE TABLE tour_scenes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tour_id BIGINT UNSIGNED NOT NULL,
    scene_id BIGINT UNSIGNED NOT NULL,
    step_order INT NOT NULL,
    narration TEXT NULL,       -- Hướng dẫn cho bước này
    duration_seconds INT NULL, -- Thời gian gợi ý dừng

    CONSTRAINT fk_ts_tour FOREIGN KEY (tour_id)
        REFERENCES tours(id) ON DELETE CASCADE,
    CONSTRAINT fk_ts_scene FOREIGN KEY (scene_id)
        REFERENCES scenes(id) ON DELETE CASCADE,
    UNIQUE KEY uq_tour_step (tour_id, step_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 8. SỔ LƯU BÚT / BỘ SƯU TẬP CÁ NHÂN
-- =====================================================================
CREATE TABLE user_collections (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    artifact_id BIGINT UNSIGNED NULL,
    scene_id BIGINT UNSIGNED NULL,
    note TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_uc_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_uc_artifact FOREIGN KEY (artifact_id)
        REFERENCES artifacts(id) ON DELETE SET NULL,
    CONSTRAINT fk_uc_scene FOREIGN KEY (scene_id)
        REFERENCES scenes(id) ON DELETE SET NULL,
    INDEX idx_uc_user (user_id, created_at),
    -- Ràng buộc: phải có ít nhất 1 trong 2 (artifact hoặc scene)
    CONSTRAINT chk_uc_target CHECK (artifact_id IS NOT NULL OR scene_id IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 9. LOG HÀNH VI THAM QUAN
-- =====================================================================
CREATE TABLE tour_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NULL,           -- NULL nếu khách ẩn danh
    session_id VARCHAR(100) NOT NULL,       -- UUID phiên
    scene_id BIGINT UNSIGNED NOT NULL,
    action ENUM('view','hotspot_click','scene_change','audio_play','exit') NOT NULL,
    hotspot_id BIGINT UNSIGNED NULL,
    duration_seconds INT DEFAULT 0,
    user_agent VARCHAR(500) NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_log_session (session_id, created_at),
    INDEX idx_log_scene_action (scene_id, action),
    INDEX idx_log_time (created_at),
    INDEX idx_log_user (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 10. ĐÁNH GIÁ TOUR
-- =====================================================================
CREATE TABLE reviews (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tour_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    rating TINYINT UNSIGNED NOT NULL,
    content TEXT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rev_tour FOREIGN KEY (tour_id)
        REFERENCES tours(id) ON DELETE CASCADE,
    CONSTRAINT fk_rev_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    CHECK (rating BETWEEN 1 AND 5),
    UNIQUE KEY uq_review_user_tour (user_id, tour_id),
    INDEX idx_rev_tour (tour_id, is_approved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 11. PHÒNG THAM QUAN ĐỒNG HÀNH (MULTI-USER)
-- =====================================================================
CREATE TABLE tour_rooms (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code CHAR(8) NOT NULL UNIQUE,           -- Mã phòng (8 ký tự)
    host_user_id BIGINT UNSIGNED NULL,
    current_scene_id BIGINT UNSIGNED NULL,
    current_pitch DECIMAL(8,4) DEFAULT 0,
    current_yaw DECIMAL(8,4) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    max_participants INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,

    CONSTRAINT fk_room_host FOREIGN KEY (host_user_id)
        REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_room_scene FOREIGN KEY (current_scene_id)
        REFERENCES scenes(id) ON DELETE SET NULL,
    INDEX idx_room_code (code, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- 12. NHẬT KÝ KIỂM TOÁN (AUDIT LOG)
-- =====================================================================
CREATE TABLE audit_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    actor_id BIGINT UNSIGNED NULL,
    action VARCHAR(60) NOT NULL,
    entity VARCHAR(60) NOT NULL,
    entity_id BIGINT UNSIGNED NULL,
    changes JSON NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_user FOREIGN KEY (actor_id)
        REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_audit_entity (entity, entity_id, created_at),
    INDEX idx_audit_time (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================================
-- TÀI KHOẢN ỨNG DỤNG (không dùng root)
-- =====================================================================
-- Chú ý: lệnh này chạy với quyền root
-- CREATE USER IF NOT EXISTS 'baotang_app'@'%' IDENTIFIED BY 'MatKhauManh123!';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON baotang360.* TO 'baotang_app'@'%';
-- FLUSH PRIVILEGES;
