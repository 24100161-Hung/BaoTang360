<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Artifact extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'name', 'slug', 'description', 'image_url',
        'era', 'origin', 'material', 'dimensions', 'inventory_code',
    ];

    public function getRouteKeyName(): string
    {
        return 'slug';
    }
}
