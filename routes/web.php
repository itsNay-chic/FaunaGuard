<?php

use App\Http\Controllers\AnimalController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\HomeController;
use App\Models\Animal;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes - FaunaGuard Kalimantan
|--------------------------------------------------------------------------
|
| Rute Publik (Beranda, Katalog Satwa, API Detail Modal),
| Rute Autentikasi Admin (Login & Logout),
| serta Rute CRUD Pengelolaan Database Satwa via Eloquent ORM.
|
*/

// =========================================================================
// 1. RUTE PUBLIK: Media Informasi & Edukasi Hayati Borneo
// =========================================================================

Route::get('/', [HomeController::class, 'beranda'])->name('beranda');
Route::get('/beranda', [HomeController::class, 'beranda']);

Route::get('/katalog', [HomeController::class, 'katalog'])->name('katalog');
Route::get('/katalog-satwa', [HomeController::class, 'katalog']);

// API Detail Satwa untuk Modal Pop-up
Route::get('/api/animals/{id}', [HomeController::class, 'animalDetail'])->name('api.animals.detail');

// =========================================================================
// 2. RUTE AUTENTIKASI: Sesi Masuk & Keluar Pengelola (Admin)
// =========================================================================

Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login'])->name('login.perform');
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// =========================================================================
// 3. RUTE CRUD PENGELOLAAN DATABASE: Hanya Dapat Diakses Oleh Admin Terautentikasi
// =========================================================================

Route::middleware('auth')->group(function () {
    Route::prefix('manage')->group(function () {
        Route::get('/', [AnimalController::class, 'index'])->name('animals.manage');
    });

    Route::resource('animals', AnimalController::class)->except(['show', 'index']);

    // Backward compatibility alias jika URL lama diakses
    Route::get('/animals/add', function () {
        return redirect()->route('animals.create');
    });
    Route::get('/animals/edit/{animal}', function (Animal $animal) {
        return redirect()->route('animals.edit', $animal);
    });
});
