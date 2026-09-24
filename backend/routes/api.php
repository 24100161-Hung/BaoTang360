<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\Api\SceneController;
use App\Http\Controllers\Api\TourController;
use App\Http\Controllers\Api\TourLogController;
use App\Http\Controllers\Api\UserCollectionController;
use App\Http\Controllers\Admin\SceneAdminController;
use Illuminate\Support\Facades\Route;

// ===== AUTH =====
Route::post("login", [AuthController::class, "login"])
    ->middleware("throttle:5,1");

// ===== PUBLIC API v1 =====
Route::prefix("v1")->group(function () {
    Route::get("scenes", [SceneController::class, "index"]);
    Route::get("scenes/{slug}", [SceneController::class, "show"]);
    Route::get("tours", [TourController::class, "index"]);
    Route::get("tours/{slug}", [TourController::class, "show"]);
    Route::post("logs", [TourLogController::class, "store"])
        ->middleware("throttle:120,1");

    Route::middleware("auth:sanctum")->group(function () {
        Route::get("me", [AuthController::class, "me"]);
        Route::get("me/collections", [UserCollectionController::class, "index"]);
        Route::post("me/collections", [UserCollectionController::class, "store"]);
        Route::delete("me/collections/{collection}", [UserCollectionController::class, "destroy"]);
    });
});

Route::middleware("auth:sanctum")->group(function () {
    Route::post("logout", [AuthController::class, "logout"]);
});

// ===== ADMIN =====
Route::middleware(["auth:sanctum", "role:admin,curator"])
    ->prefix("admin")
    ->group(function () {
        Route::get("scenes", [SceneAdminController::class, "index"]);
        Route::post("scenes", [SceneAdminController::class, "store"]);
        Route::get("scenes/{scene}", [SceneAdminController::class, "show"]);
        Route::put("scenes/{scene}", [SceneAdminController::class, "update"]);
        Route::delete("scenes/{scene}", [SceneAdminController::class, "destroy"]);
        Route::post("scenes/{scene}/upload", [SceneAdminController::class, "uploadImage"]);
    });
