<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Scene;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class SceneController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Scene::where('is_published', true)
            ->orderBy('default_order');

        if ($request->filled('q')) {
            $q = $request->input('q');
            $query->where(function ($sub) use ($q) {
                $sub->where('title', 'like', "%{$q}%")
                    ->orWhere('description', 'like', "%{$q}%");
            });
        }

        $scenes = $query->get()->map(fn($s) => [
            'id' => $s->id,
            'title' => $s->title,
            'slug' => $s->slug,
            'description' => $s->description,
            'thumb' => $s->original_image_url,
            'order' => $s->default_order,
            'tiles_status' => $s->tiles_status,
        ]);

        return response()->json(['data' => $scenes]);
    }

    public function show(string $slug): JsonResponse
    {
        $scene = Scene::where('slug', $slug)
            ->where('is_published', true)
            ->with([
                'hotspots.artifact',
                'hotspots.targetScene:id,slug,title',
                'audioGuides',
            ])
            ->firstOrFail();

        return response()->json([
            'data' => [
                'id' => $scene->id,
                'title' => $scene->title,
                'slug' => $scene->slug,
                'description' => $scene->description,
                'panorama' => $this->buildPanoramaConfig($scene),
                'hotspots' => $scene->hotspots->map(fn($h) => [
                    'id' => $h->id,
                    'type' => $h->type,
                    'pitch' => $h->pitch,
                    'yaw' => $h->yaw,
                    'title' => $h->title,
                    'content' => $h->content,
                    'icon_class' => $h->icon_class,
                    'target_scene' => $h->targetScene ? [
                        'slug' => $h->targetScene->slug,
                        'title' => $h->targetScene->title,
                    ] : null,
                    'artifact' => $h->artifact ? [
                        'id' => $h->artifact->id,
                        'name' => $h->artifact->name,
                        'image_url' => $h->artifact->image_url,
                        'era' => $h->artifact->era,
                    ] : null,
                ]),
                'audio_guides' => $scene->audioGuides->map(fn($a) => [
                    'language' => $a->language_code,
                    'name' => $a->language_name,
                    'url' => $a->audio_url,
                    'transcript' => $a->transcript,
                ]),
            ],
        ]);
    }

    private function buildPanoramaConfig(Scene $scene): array
    {
        if ($scene->tiles_status === 'done' && $scene->tiles_path) {
            return [
                'type' => 'multires',
                'path' => rtrim($scene->tiles_path, '/') . '/%l/%s%y_%x',
                'fallbackPath' => rtrim($scene->tiles_path, '/') . '/fallback/%s',
                'extension' => 'jpg',
                'tileResolution' => 512,
                'maxLevel' => 3,
                'cubeResolution' => 4096,
                'initialPitch' => $scene->initial_pitch,
                'initialYaw' => $scene->initial_yaw,
                'initialHfov' => $scene->initial_hfov,
            ];
        }

        return [
            'type' => 'equirectangular',
            'panorama' => $scene->original_image_url,
            'initialPitch' => $scene->initial_pitch,
            'initialYaw' => $scene->initial_yaw,
            'initialHfov' => $scene->initial_hfov,
        ];
    }
}
