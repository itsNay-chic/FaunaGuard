<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        User::updateOrCreate(
            ['email' => 'admin@faunaguard.org'],
            [
                'name' => 'Admin FaunaGuard',
                'password' => Hash::make('admin123'),
                'email_verified_at' => now(),
            ]
        );
    }
}

