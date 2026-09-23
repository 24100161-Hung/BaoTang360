<?php

namespace App\Console\Commands;

use App\Models\Scene;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Storage;

class GenerateSceneTiles extends Command
{
    protected $signature = 'scene:generate-tiles
                            {scene? : ID của scene (bỏ trống = tất cả pending)}
                            {--force : Xử lý lại scene đã done}
                            {--tile-size=512 : Kích thước tile}
                            {--depth=3 : Số cấp độ zoom}';

    protected $description = 'Tạo tiles đa phân giải cho ảnh 360° của scene';

    public function handle(): int
    {
        $sceneId = $this->argument('scene');

        $query = Scene::query();
        if ($sceneId) {
            $query->where('id', $sceneId);
        } elseif (!$this->option('force')) {
            $query->whereIn('tiles_status', ['pending', 'failed']);
        }

        $scenes = $query->get();

        if ($scenes->isEmpty()) {
            $this->info('Không có scene nào cần xử lý.');
            return 0;
        }

        $this->info("Sẽ xử lý {$scenes->count()} scene(s).");

        foreach ($scenes as $scene) {
            $this->processScene($scene);
        }

        return 0;
    }

    private function processScene(Scene $scene): void
    {
        $this->info("→ Scene #{$scene->id}: {$scene->title}");

        // Đánh dấu đang xử lý
        $scene->update(['tiles_status' => 'processing']);

        try {
            // Đường dẫn ảnh gốc (trong storage/app/public)
            $imagePath = $this->resolveImagePath($scene->original_image_url);

            if (!file_exists($imagePath)) {
                throw new \RuntimeException("Không tìm thấy ảnh: {$imagePath}");
            }

            // Thư mục output tiles
            $tilesDir = storage_path("app/public/tiles/scene_{$scene->id}");
            @mkdir($tilesDir, 0755, true);

            // Gọi script Python
            $scriptPath = base_path('../tools/process_panorama.py');
            if (!file_exists($scriptPath)) {
                $scriptPath = base_path('tools/process_panorama.py');
            }

            $result = Process::timeout(1800) // 30 phút
                ->run([
                    'python3', $scriptPath,
                    $imagePath,
                    $tilesDir,
                    '--tile-size', $this->option('tile-size'),
                    '--depth', $this->option('depth'),
                ]);

            if ($result->failed()) {
                throw new \RuntimeException(
                    "Script thất bại: " . $result->errorOutput()
                );
            }

            // Cập nhật DB
            $scene->update([
                'tiles_path' => "/storage/tiles/scene_{$scene->id}",
                'tiles_status' => 'done',
            ]);

            $this->info("  ✓ Hoàn thành: {$scene->tiles_path}");

        } catch (\Throwable $e) {
            $scene->update(['tiles_status' => 'failed']);
            $this->error("  ✗ Lỗi: {$e->getMessage()}");
        }
    }

    private function resolveImagePath(string $url): string
    {
        // URL dạng /storage/panoramas/xxx.jpg → storage/app/public/panoramas/xxx.jpg
        $relative = str_replace('/storage/', '', $url);
        return storage_path("app/public/{$relative}");
    }
}
