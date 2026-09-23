<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Tour extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'title', 'slug', 'description', 'cover_image_url',
        'duration_estimate_minutes', 'difficulty', 'is_published', 'created_by',
    ];

    protected $casts = [
        'is_published' => 'boolean',
    ];

    public function tourScenes(): HasMany
    {
        return $this->hasMany(TourScene::class)->orderBy('step_order');
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }
}
