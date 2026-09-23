<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\TourLog;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class TourLogController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'scene_id' => 'required|integer|exists:scenes,id',
            'action' => 'required|in:view,hotspot_click,scene_change,audio_play,exit',
            'hotspot_id' => 'nullable|integer|exists:hotspots,id',
            'duration_seconds' => 'integer|min:0|max:7200',
            'session_id' => 'required|string|max:100',
        ]);

        $data['user_id'] = auth()->id();
        $data['user_agent'] = substr($request->userAgent() ?? '', 0, 500);
        $data['ip_address'] = $request->ip();

        TourLog::create($data);

        return response()->json(['status' => 'logged'], 201);
    }
}
