<?php

use App\Http\Controllers\Api\SceneController;
use App\Http\Controllers\Api\TourController;
use App\Http\Controllers\Api\TourLogController;
use App\Http\Controllers\Api\UserCollectionController;
use App\Http\Controllers\AuthController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function () {

    // ===== Auth =====
    Route::post('login', [AuthController::class, 'login'])
        ->middleware('throttle:5,1');

    Route::middleware('auth:sanctum')->group(function () {
        Route::post('logout', [AuthController::class, 'logout']);
        Route::get('me', [AuthController::class, 'me']);

        // User collections
        Route::get('me/collections', [UserCollectionController::class, 'index']);
        Route::post('me/collections', [UserCollectionController::class, 'store']);
        Route::delete('me/collections/{collection}', [UserCollectionController::class, 'destroy']);
    });

    // ===== Public =====
    Route::get('scenes', [SceneController::class, 'index']);
    Route::get('scenes/{slug}', [SceneController::class, 'show']);
    Route::get('tours', [TourController::class, 'index']);
    Route::get('tours/{slug}', [TourController::class, 'show']);

    // Tour logs (không cần đăng nhập)
    Route::post('logs', [TourLogController::class, 'store'])
        ->middleware('throttle:120,1');
});
