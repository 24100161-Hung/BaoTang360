<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AudioGuide extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'scene_id', 'language_code', 'language_name',
        'audio_url', 'transcript', 'duration_seconds',
    ];
}
