<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class HabitatSeeder extends Seeder
{
    public function run(): void
    {
        $habitats = [
            [
                'id' => 1,
                'nama_habitat' => 'Taman Nasional Tanjung Puting',
                'lokasi' => 'Kotawaringin Barat, Kalimantan Tengah',
                'tipe_ekosistem' => 'Hutan Rawa Gambut & Hutan Tropis',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 2,
                'nama_habitat' => 'Taman Nasional Kutai',
                'lokasi' => 'Kutai Timur & Bontang, Kalimantan Timur',
                'tipe_ekosistem' => 'Hutan Hujan Dataran Rendah & Bakau',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 3,
                'nama_habitat' => 'Hutan Lindung Kutai Barat',
                'lokasi' => 'Kutai Barat, Kalimantan Timur',
                'tipe_ekosistem' => 'Hutan Hujan Tropis Pedalaman',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 4,
                'nama_habitat' => 'Taman Nasional Kayan Mentarang',
                'lokasi' => 'Kalimantan Utara, Malinau',
                'tipe_ekosistem' => 'Hutan Hujan Pegunungan Dataran Tinggi',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 5,
                'nama_habitat' => 'Taman Nasional Betung Kerihun',
                'lokasi' => 'Kapuas Hulu, Kalimantan Barat',
                'tipe_ekosistem' => 'Hutan Pegunungan & Perbukitan Batuan',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 6,
                'nama_habitat' => 'Taman Nasional Danau Sentarum',
                'lokasi' => 'Kapuas Hulu, Kalimantan Barat',
                'tipe_ekosistem' => 'Lahan Basah & Hutan Rawa Gambut',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('habitats')->upsert($habitats, ['id'], ['nama_habitat', 'lokasi', 'tipe_ekosistem', 'updated_at']);
    }
}
