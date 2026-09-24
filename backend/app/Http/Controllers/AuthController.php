<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $request->validate([
            "email" => "required|email",
            "password" => "required|string|min:6",
        ]);

        $user = User::where("email", $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password_hash)) {
            return response()->json([
                "message" => "Thông tin đăng nhập không đúng.",
            ], 401);
        }

        if ($user->status === "locked") {
            return response()->json([
                "message" => "Tài khoản đã bị khóa.",
            ], 403);
        }

        $user->tokens()->delete();
        $token = $user->createToken("admin-token")->plainTextToken;
        $user->update(["last_login_at" => now()]);

        return response()->json([
            "token" => $token,
            "user" => [
                "id" => $user->id,
                "email" => $user->email,
                "full_name" => $user->full_name,
                "role" => $user->role,
            ],
        ]);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(["status" => "logged_out"]);
    }

    public function me(Request $request)
    {
        return response()->json($request->user());
    }
}
