# 🌿 FaunaGuard — Suaka Informasi Satwa Dilindungi Kalimantan

Web portal edukasi dan inventaris konservasi satwa dilindungi di Pulau Kalimantan yang dibangun dengan fokus utama pada **arsitektur database relasional MySQL**, integritas referensial (Foreign Key), serta kemudahan inspeksi langsung menggunakan **MySQL Workbench**.

---

## 🎨 Palet Warna Khusus (Borneo Rainforest Palette)
Aplikasi ini dirancang dengan tema warna hutan hujan Kalimantan:
* **`#186049`** (*Deep Rainforest Green*): Navbar, footer, heading judul utama.
* **`#4A943E`** (*Lush Jungle Green*): Aksen alam, lencana habitat, indikator statistik.
* **`#ECE8AF`** (*Pale Sand*): Latar belakang web, kartu informasi, batas lembut yang nyaman di mata.
* **`#D98327`** (*Orangutan Amber*): Tombol Call-to-Action (CTA), lencana status kritis (CR), dan aksen interaktif.

---

## 📁 Struktur Direktori Proyek

```text
faunaguard/
├── database/
│   └── faunaguard_schema.sql  # Script DDL tabel relasional + Seeder satwa Kalimantan
├── static/
│   ├── css/
│   │   └── style.css          # Styling CSS dengan palet 4 warna khusus
│   └── js/
│       └── main.js            # Interaktivitas modal detail satwa & konfirmasi aksi
├── templates/
│   ├── base.html              # Layout utama (Navbar, Footer, Bootstrap 5 CDN)
│   ├── index.html             # Halaman publik (Hero edukasi, Statistik, Kartu Satwa, Modal)
│   ├── manage.html            # Panel CRUD data satwa (Read tabular view)
│   ├── add_animal.html        # Form Create satwa baru dengan dropdown relasi
│   ├── edit_animal.html       # Form Update satwa dengan data pre-filled
│   └── setup_notice.html      # Tampilan bantuan jika koneksi database belum disiapkan
├── .env                       # File konfigurasi koneksi database MySQL lokal
├── .env.example               # Contoh template konfigurasi
├── app.py                     # Server backend Flask & rute pengolahan SQL
├── db.py                      # Modul koneksi PyMySQL
└── requirements.txt           # Daftar dependensi Python
```

---

## 🗄️ Langkah 1: Eksekusi Database di MySQL Workbench

Sebelum menjalankan web, siapkan skema database di MySQL Workbench:

1. **Buka Aplikasi MySQL Workbench**:
   * Klik koneksi lokal Anda (misalnya `Local instance MySQL80` pada host `127.0.0.1:3306`).
2. **Buka Script SQL FaunaGuard**:
   * Klik menu **File** $\rightarrow$ **Open SQL Script...** (atau tekan `Ctrl + Shift + O`).
   * Arahkan ke file:
     `C:\Users\ASUS\.gemini\antigravity\scratch\faunaguard\database\faunaguard_schema.sql`
3. **Jalankan Script (Execute)**:
   * Klik ikon **Petir Kuning ⚡** (*Execute the selected portion of the script or everything*).
   * Panel bawah (*Output*) akan menampilkan centang hijau tanda berhasil membuat database `faunaguard_db`, 4 tabel, dan seeder data satwanya.
4. **Melihat Diagram Relasi Visual (EER Diagram)**:
   * Di menu atas MySQL Workbench, pilih **Database** $\rightarrow$ **Reverse Engineer...** (atau tekan `Ctrl + R`).
   * Klik **Next** $\rightarrow$ pilih schema **`faunaguard_db`** $\rightarrow$ klik **Next** hingga selesai.
   * MySQL Workbench akan otomatis menghasilkan diagram relasi visual lengkap dengan garis Foreign Key antara tabel `animals`, `categories`, `conservation_statuses`, dan `habitats`.

---

## 🚀 Langkah 2: Konfigurasi & Menjalankan Aplikasi Web

Karena komputer Anda telah terpasang **Python 3.13**, Anda dapat langsung menjalankannya dengan mudah:

1. **Buka File `.env`**:
   Buka file `.env` yang berada di folder `faunaguard/` dengan teks editor. Pastikan password MySQL Anda sesuai:
   ```ini
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=password_mysql_anda  # Ubah jika user root Anda menggunakan password
   DB_NAME=faunaguard_db
   PORT=5000
   ```

2. **Jalankan Aplikasi Web**:
   Buka terminal PowerShell, masuk ke folder proyek, dan jalankan:
   ```powershell
   cd C:\Users\ASUS\.gemini\antigravity\scratch\faunaguard
   python app.py
   ```

3. **Akses di Browser**:
   Buka peramban (Chrome / Edge / Firefox) dan kunjungi:
   👉 **http://127.0.0.1:5000**

---

## 🔍 Arsitektur & Relasi Tabel MySQL

* **`categories`** (Kategori Taksonomi): `id` (PK), `nama_kategori`, `deskripsi`.
* **`conservation_statuses`** (Status Konservasi IUCN): `id` (PK), `kode`, `nama_status`, `warna_badge`, `tingkat_ancaman`.
* **`habitats`** (Kawasan Konservasi Kalimantan): `id` (PK), `nama_habitat`, `lokasi`, `tipe_ekosistem`.
* **`animals`** (Data Inti Satwa):
  * `id` (PK)
  * `nama_lokal`, `nama_ilmiah`, `deskripsi`, `ancaman_utama`, `estimasi_populasi`, `foto_url`
  * `category_id` $\rightarrow$ `categories(id)` via Foreign Key
  * `status_id` $\rightarrow$ `conservation_statuses(id)` via Foreign Key
  * `habitat_id` $\rightarrow$ `habitats(id)` via Foreign Key
