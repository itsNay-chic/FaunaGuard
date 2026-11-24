<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CategorySeeder extends Seeder
{
    public function run(): void
    {
        $categories = [
            [
                'id' => 1,
                'nama_kategori' => 'Mamalia',
                'deskripsi' => 'Hewan menyusui bertulang belakang yang berdarah panas, sebagian besar berhabitat di hutan tropis dan sungai Kalimantan.',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 2,
                'nama_kategori' => 'Aves',
                'deskripsi' => 'Kelompok burung dan unggas berbulu yang memiliki peran penting dalam penyebaran biji pohon hutan kanopi Kalimantan.',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 3,
                'nama_kategori' => 'Reptilia',
                'deskripsi' => 'Hewan melata berdarah dingin bersisik, mendiami rawa gambut dan perairan tawar Pulau Borneo.',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('categories')->upsert($categories, ['id'], ['nama_kategori', 'deskripsi', 'updated_at']);
    }
}

