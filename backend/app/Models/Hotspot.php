<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Hotspot extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'scene_id', 'type', 'pitch', 'yaw', 'title', 'content',
        'target_scene_id', 'artifact_id', 'icon_class', 'display_order',
    ];

    protected $casts = [
        'pitch' => 'float',
        'yaw' => 'float',
    ];

    public function scene(): BelongsTo
    {
        return $this->belongsTo(Scene::class);
    }

    public function targetScene(): BelongsTo
    {
        return $this->belongsTo(Scene::class, 'target_scene_id');
    }

    public function artifact(): BelongsTo
    {
        return $this->belongsTo(Artifact::class);
    }
}
