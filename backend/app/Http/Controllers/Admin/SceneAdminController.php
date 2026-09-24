<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Scene;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class SceneAdminController extends Controller
{
    public function index(Request $request)
    {
        $query = Scene::orderBy('default_order');

        if ($request->filled('q')) {
            $query->where('title', 'like', '%' . $request->input('q') . '%');
        }

        $scenes = $query->paginate(20);

        return response()->json($scenes);
    }

    public function show(Scene $scene)
    {
        return response()->json(['data' => $scene->load('hotspots', 'audioGuides')]);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'title' => 'required|string|max:200',
            'description' => 'nullable|string',
            'slug' => 'nullable|string|max:220|unique:scenes,slug',
            'initial_pitch' => 'nullable|numeric|between:-90,90',
            'initial_yaw' => 'nullable|numeric|between:-180,180',
            'initial_hfov' => 'nullable|numeric|between:30,120',
            'default_order' => 'nullable|integer|min:0',
        ]);

        if (empty($data['slug'])) {
            $data['slug'] = Str::slug($data['title']);
        }

        $data['created_by'] = auth()->id();
        $data['tiles_status'] = 'pending';

        $scene = Scene::create($data);

        return response()->json(['data' => $scene], 201);
    }

    public function update(Request $request, Scene $scene)
    {
        $data = $request->validate([
            'title' => 'sometimes|string|max:200',
            'description' => 'nullable|string',
            'initial_pitch' => 'nullable|numeric|between:-90,90',
            'initial_yaw' => 'nullable|numeric|between:-180,180',
            'initial_hfov' => 'nullable|numeric|between:30,120',
            'default_order' => 'nullable|integer|min:0',
            'is_published' => 'boolean',
        ]);

        $scene->update($data);

        return response()->json(['data' => $scene]);
    }

    public function destroy(Scene $scene)
    {
        // Xóa file ảnh
        if ($scene->original_image_url) {
            $path = str_replace('/storage/', '', $scene->original_image_url);
            Storage::disk('public')->delete($path);
        }

        // Xóa tiles
        if ($scene->tiles_path) {
            $tilesDir = str_replace('/storage/', '', $scene->tiles_path);
            Storage::disk('public')->deleteDirectory($tilesDir);
        }

        $scene->delete();

        return response()->json(['status' => 'deleted']);
    }

    /**
     * Upload ảnh 360° cho scene
     */
    public function uploadImage(Request $request, Scene $scene)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,jpg,png|max:51200', // 50MB
        ]);

        try {
            // Xóa ảnh cũ
            if ($scene->original_image_url) {
                $oldPath = str_replace('/storage/', '', $scene->original_image_url);
                Storage::disk('public')->delete($oldPath);
            }

            // Lưu ảnh mới
            $file = $request->file('image');
            $filename = $scene->slug . '-' . time() . '.' . $file->getClientOriginalExtension();
            $path = $file->storeAs('panoramas', $filename, 'public');

            $scene->update([
                'original_image_url' => "/storage/{$path}",
                'tiles_status' => 'pending',
                'tiles_path' => null,
            ]);

            return response()->json([
                'status' => 'uploaded',
                'data' => [
                    'image_url' => $scene->original_image_url,
                    'tiles_status' => 'pending',
                ],
            ]);
        } catch (\Throwable $e) {
            return response()->json([
                'message' => 'Upload thất bại: ' . $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Sinh tiles cho scene
     */
    public function generateTiles(Scene $scene)
    {
        if (!$scene->original_image_url) {
            return response()->json(['message' => 'Scene chưa có ảnh'], 422);
        }

        // Đánh dấu đang xử lý
        $scene->update(['tiles_status' => 'processing']);

        try {
            $imagePath = str_replace('/storage/', '', $scene->original_image_url);
            $fullPath = storage_path("app/public/{$imagePath}");

            if (!file_exists($fullPath)) {
                throw new \RuntimeException("Không tìm thấy file ảnh: {$fullPath}");
            }

            $tilesDir = storage_path("app/public/tiles/scene_{$scene->id}");
            @mkdir($tilesDir, 0755, true);

            // Gọi script Python
            $scriptPath = base_path('../tools/process_panorama.py');

            $cmd = "python3 " . escapeshellarg($scriptPath) . " "
                 . escapeshellarg($fullPath) . " "
                 . escapeshellarg($tilesDir) . " "
                 . "--tile-size 512 --depth 3 2>&1";

            exec($cmd, $output, $returnCode);

            if ($returnCode !== 0) {
                throw new \RuntimeException("Script thất bại: " . implode("\n", $output));
            }

            $scene->update([
                'tiles_path' => "/storage/tiles/scene_{$scene->id}",
                'tiles_status' => 'done',
            ]);

            return response()->json([
                'status' => 'done',
                'output' => $output,
                'data' => $scene,
            ]);
        } catch (\Throwable $e) {
            $scene->update(['tiles_status' => 'failed']);

            return response()->json([
                'message' => 'Sinh tiles thất bại: ' . $e->getMessage(),
                'status' => 'failed',
            ], 500);
        }
    }
}
