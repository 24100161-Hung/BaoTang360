<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Scene extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'title', 'slug', 'description', 'original_image_url',
        'tiles_path', 'tiles_status',
        'initial_pitch', 'initial_yaw', 'initial_hfov',
        'default_order', 'is_published', 'created_by',
    ];

    protected $casts = [
        'initial_pitch' => 'float',
        'initial_yaw' => 'float',
        'initial_hfov' => 'float',
        'is_published' => 'boolean',
    ];

    public function hotspots(): HasMany
    {
        return $this->hasMany(Hotspot::class)->orderBy('display_order');
    }

    public function audioGuides(): HasMany
    {
        return $this->hasMany(AudioGuide::class);
    }

    public function creator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }
}
