<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Tour;
use Illuminate\Http\JsonResponse;

class TourController extends Controller
{
    public function index(): JsonResponse
    {
        $tours = Tour::where('is_published', true)
            ->withCount('tourScenes')
            ->orderByDesc('created_at')
            ->get()
            ->map(fn($t) => [
                'id' => $t->id,
                'title' => $t->title,
                'slug' => $t->slug,
                'description' => $t->description,
                'cover' => $t->cover_image_url,
                'duration' => $t->duration_estimate_minutes,
                'difficulty' => $t->difficulty,
                'scene_count' => $t->tour_scenes_count,
            ]);

        return response()->json(['data' => $tours]);
    }

    public function show(string $slug): JsonResponse
    {
        $tour = Tour::where('slug', $slug)
            ->where('is_published', true)
            ->with(['tourScenes.scene:id,slug,title,original_image_url'])
            ->firstOrFail();

        return response()->json([
            'data' => [
                'id' => $tour->id,
                'title' => $tour->title,
                'slug' => $tour->slug,
                'description' => $tour->description,
                'cover' => $tour->cover_image_url,
                'duration' => $tour->duration_estimate_minutes,
                'difficulty' => $tour->difficulty,
                'steps' => $tour->tourScenes->map(fn($ts) => [
                    'order' => $ts->step_order,
                    'scene_slug' => $ts->scene->slug,
                    'scene_title' => $ts->scene->title,
                    'narration' => $ts->narration,
                    'duration' => $ts->duration_seconds,
                ]),
            ],
        ]);
    }
}
