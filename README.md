# Bảo tàng ảo 360° - CSE703073

Hệ thống tham quan bảo tàng ảo với công nghệ 360° panorama.

## Ngăn xếp công nghệ
- Backend: PHP 8.3 / Laravel 11
- Frontend: Vue 3 + Vite + Pannellum
- Database: MySQL 8.0
- Python: FastAPI + pandas + scikit-learn
- Web server: Nginx
- Container: Docker Compose

## Cài đặt nhanh
```bash
cp .env.example .env
docker compose up -d --build
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate --seed
# Mở http://localhost:8080
