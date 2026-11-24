<?php

namespace App\Services;

use App\Models\Animal;
use App\Models\Category;
use App\Models\ConservationStatus;
use App\Models\Habitat;
use Illuminate\Support\Facades\Log;

class DatabaseSyncService
{
    /**
     * Format nilai ke literal SQL yang aman.
     */
    protected static function sqlFormatValue($val): string
    {
        if (is_null($val)) {
            return 'NULL';
        }
        if (is_int($val) || is_float($val)) {
            return (string) $val;
        }

        $escaped = str_replace(['\\', "'"], ['\\\\', "''"], (string) $val);

        return "'{$escaped}'";
    }

    /**
     * Ekspor seluruh data tabel ke database/faunaguard_schema.sql
     */
    public static function exportToSqlFile(): bool
    {
        try {
            $categories = Category::orderBy('id', 'ASC')->get();
            $statuses = ConservationStatus::orderBy('id', 'ASC')->get();
            $habitats = Habitat::orderBy('id', 'ASC')->get();
            $animals = Animal::orderBy('id', 'ASC')->get();

            $lines = [
                '-- =============================================================================',
                '-- FaunaGuard: Database Relasional MySQL Konservasi Satwa Dilindungi Kalimantan',
                '-- File ini diperbarui secara OTOMATIS saat data diubah melalui aplikasi web.',
                '-- =============================================================================',
                '',
                'CREATE DATABASE IF NOT EXISTS faunaguard_db ',
                '    CHARACTER SET utf8mb4 ',
                '    COLLATE utf8mb4_unicode_ci;',
                '',
                'USE faunaguard_db;',
                '',
                'SET FOREIGN_KEY_CHECKS = 0;',
                'DROP TABLE IF EXISTS animals;',
                'DROP TABLE IF EXISTS habitats;',
                'DROP TABLE IF EXISTS conservation_statuses;',
                'DROP TABLE IF EXISTS categories;',
                'SET FOREIGN_KEY_CHECKS = 1;',
                '',
                'CREATE TABLE categories (',
                '    id INT AUTO_INCREMENT PRIMARY KEY,',
                '    nama_kategori VARCHAR(50) NOT NULL UNIQUE,',
                '    deskripsi TEXT NULL',
                ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;',
                '',
                'CREATE TABLE conservation_statuses (',
                '    id INT AUTO_INCREMENT PRIMARY KEY,',
                '    kode VARCHAR(10) NOT NULL UNIQUE,',
                '    nama_status VARCHAR(50) NOT NULL,',
                '    warna_badge VARCHAR(20) DEFAULT \'#D98327\',',
                '    tingkat_ancaman VARCHAR(50) NOT NULL',
                ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;',
                '',
                'CREATE TABLE habitats (',
                '    id INT AUTO_INCREMENT PRIMARY KEY,',
                '    nama_habitat VARCHAR(100) NOT NULL,',
                '    lokasi VARCHAR(100) NOT NULL,',
                '    tipe_ekosistem VARCHAR(50) NOT NULL',
                ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;',
                '',
                'CREATE TABLE animals (',
                '    id INT AUTO_INCREMENT PRIMARY KEY,',
                '    nama_lokal VARCHAR(100) NOT NULL,',
                '    nama_ilmiah VARCHAR(100) NOT NULL,',
                '    deskripsi TEXT NULL,',
                '    ancaman_utama TEXT NULL,',
                '    estimasi_populasi INT NULL,',
                '    category_id INT NOT NULL,',
                '    status_id INT NOT NULL,',
                '    habitat_id INT NOT NULL,',
                '    foto_url MEDIUMTEXT NULL,',
                '    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,',
                '    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,',
                '  ',
                '    CONSTRAINT fk_animal_category ',
                '        FOREIGN KEY (category_id) REFERENCES categories (id) ',
                '        ON UPDATE CASCADE ON DELETE RESTRICT,',
                '        ',
                '    CONSTRAINT fk_animal_status ',
                '        FOREIGN KEY (status_id) REFERENCES conservation_statuses (id) ',
                '        ON UPDATE CASCADE ON DELETE RESTRICT,',
                '        ',
                '    CONSTRAINT fk_animal_habitat ',
                '        FOREIGN KEY (habitat_id) REFERENCES habitats (id) ',
                '        ON UPDATE CASCADE ON DELETE RESTRICT',
                ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;',
                '',
                'CREATE INDEX idx_animals_nama ON animals (nama_lokal);',
                'CREATE INDEX idx_animals_category ON animals (category_id);',
                'CREATE INDEX idx_animals_status ON animals (status_id);',
                'CREATE INDEX idx_animals_habitat ON animals (habitat_id);',
                '',
            ];

            // 1. Categories
            if ($categories->isNotEmpty()) {
                $lines[] = 'INSERT INTO categories (id, nama_kategori, deskripsi) VALUES';
                $catRows = [];
                foreach ($categories as $c) {
                    $catRows[] = "({$c->id}, ".self::sqlFormatValue($c->nama_kategori).', '.self::sqlFormatValue($c->deskripsi).')';
                }
                $lines[] = implode(",\n", $catRows).";\n";
            }

            // 2. Conservation Statuses
            if ($statuses->isNotEmpty()) {
                $lines[] = 'INSERT INTO conservation_statuses (id, kode, nama_status, warna_badge, tingkat_ancaman) VALUES';
                $stRows = [];
                foreach ($statuses as $s) {
                    $stRows[] = "({$s->id}, ".self::sqlFormatValue($s->kode).', '.self::sqlFormatValue($s->nama_status).', '.self::sqlFormatValue($s->warna_badge).', '.self::sqlFormatValue($s->tingkat_ancaman).')';
                }
                $lines[] = implode(",\n", $stRows).";\n";
            }

            // 3. Habitats
            if ($habitats->isNotEmpty()) {
                $lines[] = 'INSERT INTO habitats (id, nama_habitat, lokasi, tipe_ekosistem) VALUES';
                $habRows = [];
                foreach ($habitats as $h) {
                    $habRows[] = "({$h->id}, ".self::sqlFormatValue($h->nama_habitat).', '.self::sqlFormatValue($h->lokasi).', '.self::sqlFormatValue($h->tipe_ekosistem).')';
                }
                $lines[] = implode(",\n", $habRows).";\n";
            }

            // 4. Animals
            if ($animals->isNotEmpty()) {
                $lines[] = 'INSERT INTO animals (';
                $lines[] = '    id, nama_lokal, nama_ilmiah, deskripsi, ancaman_utama,';
                $lines[] = '    estimasi_populasi, category_id, status_id, habitat_id, foto_url';
                $lines[] = ') VALUES';
                $animalRows = [];
                foreach ($animals as $a) {
                    $row = "(\n"
                        ."    {$a->id},\n"
                        .'    '.self::sqlFormatValue($a->nama_lokal).",\n"
                        .'    '.self::sqlFormatValue($a->nama_ilmiah).",\n"
                        .'    '.self::sqlFormatValue($a->deskripsi).",\n"
                        .'    '.self::sqlFormatValue($a->ancaman_utama).",\n"
                        .'    '.self::sqlFormatValue($a->estimasi_populasi).",\n"
                        ."    {$a->category_id},\n"
                        ."    {$a->status_id},\n"
                        ."    {$a->habitat_id},\n"
                        .'    '.self::sqlFormatValue($a->foto_url)."\n"
                        .')';
                    $animalRows[] = $row;
                }
                $lines[] = implode(",\n", $animalRows).";\n";
            }

            // Query verifikasi relasional
            $lines[] = 'SELECT ';
            $lines[] = '    a.id,';
            $lines[] = '    a.nama_lokal,';
            $lines[] = '    a.nama_ilmiah,';
            $lines[] = '    c.nama_kategori,';
            $lines[] = '    s.kode AS status_iucn,';
            $lines[] = '    s.nama_status,';
            $lines[] = '    s.tingkat_ancaman,';
            $lines[] = '    h.nama_habitat,';
            $lines[] = '    h.lokasi AS habitat_lokasi,';
            $lines[] = '    a.estimasi_populasi,';
            $lines[] = '    a.ancaman_utama';
            $lines[] = 'FROM animals a';
            $lines[] = 'JOIN categories c ON a.category_id = c.id';
            $lines[] = 'JOIN conservation_statuses s ON a.status_id = s.id';
            $lines[] = 'JOIN habitats h ON a.habitat_id = h.id';
            $lines[] = 'ORDER BY a.id ASC;';
            $lines[] = '';

            $sqlContent = implode("\n", $lines);
            $filePath = base_path('database/faunaguard_schema.sql');
            file_put_contents($filePath, $sqlContent);

            return true;
        } catch (\Throwable $e) {
            Log::error('[FaunaGuard Sync Error] '.$e->getMessage());

            return false;
        }
    }

    /**
     * Sinkronkan file database ke GitHub repo origin main
     */
    public static function syncToGitHub(string $commitMessage = 'chore(db): sinkronisasi otomatis database ke github', bool $background = true): void
    {
        // Jangan jalankan git sync saat automated testing
        if (app()->environment('testing')) {
            return;
        }

        // 1. Selalu ekspor database ke file SQL terlebih dahulu
        self::exportToSqlFile();

        // 2. Jalankan git commit & push ke origin main
        $baseDir = escapeshellarg(base_path());
        $escapedMsg = escapeshellarg($commitMessage);

        if ($background && strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
            // Background execution di Windows cmd tanpa memblokir request browser
            $cmd = "start /B cmd /C \"cd /d {$baseDir} && git add database/faunaguard_schema.sql public/uploads && git commit -m {$escapedMsg} && git push origin main\"";
            @pclose(@popen($cmd, 'r'));
        } else {
            @exec("cd {$baseDir} && git add database/faunaguard_schema.sql public/uploads && git commit -m {$escapedMsg} && git push origin main");
        }
    }
}
