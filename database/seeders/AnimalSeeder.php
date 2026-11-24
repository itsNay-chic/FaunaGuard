<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class AnimalSeeder extends Seeder
{
    public function run(): void
    {
        $animals = [
            [
                'id' => 1,
                'nama_lokal' => 'Orangutan Kalimantan',
                'nama_ilmiah' => 'Pongo pygmaeus',
                'deskripsi' => 'Primata besar berbulu oranye kecokelatan yang menghabiskan 90% hidupnya di kanopi pohon. Merupakan "petani hutan" sejati karena perannya yang vital dalam menyebarkan biji-bijian pohon hutan hujan Kalimantan.',
                'ancaman_utama' => 'Deforestasi masif akibat alih fungsi lahan sawit, kebakaran lahan gambut, serta fragmentasi habitat oleh jalur logistik tambang.',
                'estimasi_populasi' => 57000,
                'category_id' => 1,
                'status_id' => 1,
                'habitat_id' => 1,
                'foto_url' => 'https://assets.promediateknologi.id/crop/0x0:0x0/1200x0/webp/photo/p1/776/2023/09/04/Orangutan-Kalimantan-2916502849.jpg',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 2,
                'nama_lokal' => 'Bekantan',
                'nama_ilmiah' => 'Nasalis larvatus',
                'deskripsi' => 'Monyet endemik Pulau Borneo dengan ciri khas hidung panjang menggantung dan perut buncit. Mampu berenang dengan sangat baik melintasi rawa dan sungai karena memiliki selaput di sela-sela jarinya.',
                'ancaman_utama' => 'Konversi hutan mangrove dan nipah pesisir menjadi tambak udang komersial, pencemaran air muara, serta perburuan liar sporadis.',
                'estimasi_populasi' => 16000,
                'category_id' => 1,
                'status_id' => 2,
                'habitat_id' => 2,
                'foto_url' => 'https://img.freepik.com/premium-photo/bekantan-nasalis-larvatus_1013208-580.jpg',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 3,
                'nama_lokal' => 'Badak Kalimantan',
                'nama_ilmiah' => 'Dicerorhinus sumatrensis harrissoni',
                'deskripsi' => 'Subspesies badak terkecil di dunia yang sangat pemalu dan soliter. Memiliki dua cula kecil dan tubuh berbulu kasar kemerahan. Merupakan mamalia darat paling langka di Kalimantan.',
                'ancaman_utama' => 'Populasi yang sangat kecil dan terisolasi menyulitkan perkembangbiakan alami, ancaman jerat pemburu babi hutan, serta hilangnya koridor hutan jelajah.',
                'estimasi_populasi' => 15,
                'category_id' => 1,
                'status_id' => 1,
                'habitat_id' => 3,
                'foto_url' => 'https://nomorsatukaltim.disway.id/upload/3a7ae0b37e9e91ef60222f829a1a3e4a.png',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 4,
                'nama_lokal' => 'Kucing Merah Kalimantan',
                'nama_ilmiah' => 'Catopuma badia',
                'deskripsi' => 'Spesies kucing liar endemik Pulau Kalimantan yang sangat langka dan elusif, hingga sering dijuluki sebagai "hantu hutan" oleh para peneliti. Memiliki tubuh yang ramping dengan panjang sekitar 60–70 cm dan berat berkisar antara 3–4 kg.',
                'ancaman_utama' => 'Deforestasi dan fragmentasi habitat, jerat liar, perburuan dan perdagangan ilegal, serta kepadatan populasi alami yang sangat rendah.',
                'estimasi_populasi' => 2200,
                'category_id' => 1,
                'status_id' => 2,
                'habitat_id' => 4,
                'foto_url' => 'https://1001indonesia.net/asset/2021/03/Kucing-Merah-Kalimantan.jpg',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 5,
                'nama_lokal' => 'Enggang Gading',
                'nama_ilmiah' => 'Rhinoplax vigil',
                'deskripsi' => 'Burung berukuran megah dengan bentang sayap hampir 2 meter dan helm/balung kepala padat berwarna merah menyala. Memiliki suara panggilan tawa khas yang menggema di seluruh hutan pedalaman Borneo.',
                'ancaman_utama' => 'Perburuan liar brutal untuk mengambil balung padatnya (dijuluki gading merah bernilai tinggi di pasar gelap) serta penebangan pohon beringin/ara raksasa tempat bersarang.',
                'estimasi_populasi' => 4000,
                'category_id' => 2,
                'status_id' => 1,
                'habitat_id' => 5,
                'foto_url' => 'https://tse3.mm.bing.net/th/id/OIP.LYLz50B9LE-9g4NSWSnH4gHaEK?r=0&rs=1&pid=ImgDetMain&o=7&rm=3',
                'created_at' => now(),
                'updated_at' => now(),
            ],
        ];

        DB::table('animals')->upsert($animals, ['id'], [
            'nama_lokal', 'nama_ilmiah', 'deskripsi', 'ancaman_utama',
            'estimasi_populasi', 'category_id', 'status_id', 'habitat_id',
            'foto_url', 'updated_at'
        ]);
    }
}

