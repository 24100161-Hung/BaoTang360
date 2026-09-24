<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Hotspot;
use App\Models\Scene;
use Illuminate\Http\Request;

class HotspotAdminController extends Controller
{
    public function index(Scene $scene)
    {
        return response()->json([
            'data' => $scene->hotspots()->orderBy('display_order')->get(),
        ]);
    }

    public function store(Request $request, Scene $scene)
    {
        $data = $request->validate([
            'type' => 'required|in:info,scene,artifact',
            'pitch' => 'required|numeric|between:-90,90',
            'yaw' => 'required|numeric|between:-180,180',
            'title' => 'required|string|max:200',
            'content' => 'nullable|string',
            'target_scene_id' => 'nullable|exists:scenes,id',
            'artifact_id' => 'nullable|exists:artifacts,id',
            'icon_class' => 'nullable|string|max:80',
            'display_order' => 'nullable|integer',
        ]);

        $data['scene_id'] = $scene->id;

        $hotspot = Hotspot::create($data);

        return response()->json(['data' => $hotspot], 201);
    }

    public function update(Request $request, Hotspot $hotspot)
    {
        $data = $request->validate([
            'type' => 'sometimes|in:info,scene,artifact',
            'pitch' => 'sometimes|numeric|between:-90,90',
            'yaw' => 'sometimes|numeric|between:-180,180',
            'title' => 'sometimes|string|max:200',
            'content' => 'nullable|string',
            'target_scene_id' => 'nullable|exists:scenes,id',
            'artifact_id' => 'nullable|exists:artifacts,id',
            'icon_class' => 'nullable|string|max:80',
            'display_order' => 'nullable|integer',
        ]);

        $hotspot->update($data);

        return response()->json(['data' => $hotspot]);
    }

    public function destroy(Hotspot $hotspot)
    {
        $hotspot->delete();
        return response()->json(['status' => 'deleted']);
    }
}
