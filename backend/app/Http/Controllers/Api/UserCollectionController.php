<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\UserCollection;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class UserCollectionController extends Controller
{
    public function index(): JsonResponse
    {
        $items = UserCollection::where('user_id', auth()->id())
            ->with([
                'artifact:id,name,image_url,era',
                'scene:id,slug,title,original_image_url',
            ])
            ->orderByDesc('created_at')
            ->get();

        return response()->json(['data' => $items]);
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'artifact_id' => 'nullable|integer|exists:artifacts,id',
            'scene_id' => 'nullable|integer|exists:scenes,id',
            'note' => 'nullable|string|max:2000',
        ]);

        if (empty($data['artifact_id']) && empty($data['scene_id'])) {
            return response()->json([
                'message' => 'Cần chọn hiện vật hoặc không gian',
            ], 422);
        }

        $data['user_id'] = auth()->id();
        $item = UserCollection::create($data);

        return response()->json(['data' => $item], 201);
    }

    public function destroy(UserCollection $collection): JsonResponse
    {
        if ($collection->user_id !== auth()->id()) {
            abort(403);
        }
        $collection->delete();

        return response()->json(['status' => 'deleted']);
    }
}
