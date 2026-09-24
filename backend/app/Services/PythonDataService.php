<?php

namespace App\Services;

use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class PythonDataService
{
    private string $baseUrl;
    private string $token;

    public function __construct()
    {
        $this->baseUrl = rtrim(config('services.python.url', 'http://python:8001'), '/');
        $this->token = (string) config('services.python.token', '');
    }

    public function visitorStats(): array
    {
        return $this->cachedGet('visitor-stats', 900, '/analytics/visitor-stats');
    }

    public function dropOffAnalysis(int $minSessions = 3): array
    {
        return $this->cachedGet(
            "drop-off:{$minSessions}",
            1800,
            '/analytics/drop-off',
            ['min_sessions' => $minSessions]
        );
    }

    public function topDestinations(int $limit = 10): array
    {
        return $this->cachedGet(
            "top-dest:{$limit}",
            900,
            '/analytics/top-destinations',
            ['limit' => $limit]
        );
    }

    public function sceneHeatmap(int $sceneId): array
    {
        return $this->cachedGet(
            "heatmap:{$sceneId}",
            600,
            "/analytics/scene-heatmap/{$sceneId}"
        );
    }

    public function recommendScenes(int $sceneId, int $k = 5): array
    {
        return $this->cachedGet(
            "recommend:{$sceneId}:{$k}",
            1800,
            "/recommend/scenes/{$sceneId}",
            ['k' => $k]
        );
    }

    private function cachedGet(string $key, int $ttl, string $path, array $query = []): array
    {
        return Cache::remember($key, $ttl, function () use ($path, $query) {
            try {
                $res = Http::withHeaders(['X-Service-Token' => $this->token])
                    ->timeout(5)
                    ->retry(2, 200)
                    ->get($this->baseUrl . $path, $query);

                if ($res->successful()) {
                    return $res->json('data', []);
                }

                Log::warning('Python service error', [
                    'path' => $path,
                    'status' => $res->status(),
                ]);
            } catch (\Throwable $e) {
                Log::error('Python service unavailable', [
                    'path' => $path,
                    'error' => $e->getMessage(),
                ]);
            }

            return [];
        });
    }
}
