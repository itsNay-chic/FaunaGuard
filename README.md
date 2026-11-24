# 🌿 FaunaGuard — Portal Informasi & Edukasi Satwa Dilindungi Kalimantan

> **Aplikasi Web Konservasi Keanekaragaman Hayati Hutan Hujan Tropis Borneo**  
> Dibangun menggunakan **Framework Laravel**, **PHP 8.5**, **MySQL**, **Eloquent ORM**, dan **Blade Templating**.

---

## 📌 Fitur & Modul Utama Laravel

1. **Routing (`routes/web.php`)**:
   - Rute Publik: Beranda (`/`, `/beranda`), Katalog Satwa (`/katalog`, `/katalog-satwa`), API JSON Detail Satwa (`/api/animals/{id}`).
   - Rute Autentikasi Admin: Login (`/login`) & Logout (`/logout`).
   - Rute CRUD Pengelolaan Database: Panel Kelola Data (`/manage`), Tambah Satwa (`/animals/create`), Edit Satwa (`/animals/{id}/edit`), dsb.

2. **Eloquent ORM & Relasi Database (`app/Models/`)**:
   - `Animal`: Model satwa yang terhubung dengan `Category`, `ConservationStatus`, dan `Habitat`. Dilengkapi query scopes untuk pencarian dan filter dinamis.
   - `Category`: Relasi *One-to-Many* ke satwa.
   - `ConservationStatus`: Status keterancaman IUCN (CR, EN, VU) beserta warna badge visual.
   - `Habitat`: Data kawasan konservasi dan tipe ekosistem.
   - `User`: Akun pengelola/admin terotentikasi.

3. **Database Migration & Seeding (`database/migrations/`, `database/seeders/`)**:
   - Migration terstruktur dengan *Foreign Key Constraints* (`cascadeOnUpdate`, `restrictOnDelete`).
   - Seeder otomatis memuat 5 satwa endemik Kalimantan, master kategori, master status IUCN, kawasan habitat, dan akun admin awal.

4. **Blade Templating & UI Interaktif (`resources/views/`)**:
   - Layout modular `layouts.app` dengan navigasi responsif, flash alert, dan tema hutan tropis Borneo.
   - Modal pop-up edukasi satwa interaktif dengan pemuatan data real-time via Fetch API.
   - Formulir validasi dengan penanda error visual (`@error ... @enderror`) dan pratinjau gambar langsung (*live image preview*).

5. **Form Requests & Keamanan (`app/Http/Requests/`)**:
   - `StoreAnimalRequest` & `UpdateAnimalRequest` untuk validasi kolom wajib, tipe file gambar (JPG/PNG/WEBP/GIF), dan batas ukuran upload.
   - Proteksi CSRF (`@csrf`), password hashing dengan Bcrypt, dan session authentication.

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Prasyarat Lingkungan
- **PHP** $\ge$ 8.2 (Direkomendasikan PHP 8.5)
- **Composer** $\ge$ 2.0
- **MySQL / MariaDB**

### 2. Instalasi Dependensi
```bash
composer install
```

### 3. Konfigurasi Environment (`.env`)
Salin file `.env.example` ke `.env`:
```bash
cp .env.example .env
php artisan key:generate
```
Pastikan pengaturan koneksi database MySQL di `.env` sesuai:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=faunaguard_db
DB_USERNAME=root
DB_PASSWORD=
```

### 4. Eksekusi Migration & Seeding
Jalankan migrasi tabel dan pengisian data awal ke MySQL:
```bash
php artisan migrate --seed
```

### 5. Menjalankan Server Lokal
```bash
php artisan serve
```
Buka browser Anda dan akses: **`http://127.0.0.1:8000`**

---

## 🔐 Kredensial Login Admin

Untuk mengakses fitur **Kelola Database (CRUD)**:
- **URL Login**: `http://127.0.0.1:8000/login`
- **Email**: `admin@faunaguard.org`
- **Password**: `admin123`

---

## 🧪 Menjalankan Pengujian Otomatis (Testing)
Aplikasi ini dilengkapi rangkaian uji fitur otomatis (PHPUnit / Pest):
```bash
php artisan test
```
Semua rute, query Eloquent, autentikasi, dan operasi CRUD telah terverifikasi sukses 100%.
