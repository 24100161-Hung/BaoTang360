<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TourLog extends Model
{
    public $timestamps = false;

    protected $fillable = [
        'user_id', 'session_id', 'scene_id', 'action',
        'hotspot_id', 'duration_seconds', 'user_agent', 'ip_address',
    ];
}
