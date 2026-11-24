<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class ConservationStatusSeeder extends Seeder
{
    public function run(): void
    {
        $statuses = [
            [
                'id' => 1,
                'kode' => 'CR',
                'nama_status' => 'Critically Endangered (Kritis)',
                'warna_badge' => '#D98327',
                'tingkat_ancaman' => 'Sangat Kritis Menuju Kepunahan',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 2,
                'kode' => 'EN',
                'nama_status' => 'Endangered (Terancam)',
                'warna_badge' => '#4A943E',
                'tingkat_ancaman' => 'Risiko Tinggi Kepunahan di Alam Liar',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 3,
                'kode' => 'VU',
                'nama_status' => 'Vulnerable (Rentan)',
                'warna_badge' => '#186049',
                'tingkat_ancaman' => 'Menghadapi Risiko Kepunahan Masa Depan',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('conservation_statuses')->upsert($statuses, ['id'], ['kode', 'nama_status', 'warna_badge', 'tingkat_ancaman', 'updated_at']);
    }
}

