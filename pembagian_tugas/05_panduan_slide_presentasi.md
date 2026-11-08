# 📊 Panduan Lengkap Slide Presentasi FaunaGuard (12 Slide)

Dokumen ini merupakan panduan pendamping (*slide transcript & speaker notes*) untuk file presentasi PowerPoint:  
📁 [**`pembagian_tugas/FaunaGuard_Presentasi_Web_dan_Database.pptx`**](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/pembagian_tugas/FaunaGuard_Presentasi_Web_dan_Database.pptx)

Tema Desain: **Borneo Rainforest & Wildlife Palette** (Warna Alam Hijau Hutan Hujan Tropis `#186049`, Aksen Daun `#4A943E`, Latar Krem Pasir `#FAF9F3`, dan Oranye Amber Orangutan `#D98327`).

---

## 🗂️ Rangkuman Isi Slide Presentasi

| No | Judul Slide | Kategori Pembahasan | Visual / Aset |
|:---:|---|---|---|
| **1** | **Cover**: FaunaGuard — Suaka Informasi & Edukasi Konservasi Satwa Dilindungi Kalimantan | Judul Utama | Badge tema alam, judul besar, 3 pilar utama |
| **2** | **Latar Belakang & Urgensi Hayati Borneo** | 1. Penjelasan Isi Web | 3 Card (Hutan Tertua, Ancaman Kepunahan, Solusi FaunaGuard) |
| **3** | **Struktur & Konten Utama Web FaunaGuard** | 1. Penjelasan Isi Web | Banner Pengantar + 3 Card Halaman (Beranda, Katalog, CRUD) |
| **4** | **Fitur-Fitur di Web (Bagian 1: Modul Publik & Edukasi)** | 2. Fitur di Webnya | 4 Card (Animal Cards, Filter Cepat, Modal Asinkron, Fallback SVG) |
| **5** | **Fitur-Fitur di Web (Bagian 2: CRUD & Logika Cerdas)** | 2. Fitur di Webnya | 4 Card (Tabel CRUD, Live Upload Preview, Smart URL Scraper, Setup Notice) |
| **6** | **Arsitektur Database Relasional & Normalisasi 3NF** | 3. Penjelasan Database | Card Alasan 3NF + 4 Card Tabel (`categories`, `statuses`, `habitats`, `animals`) |
| **7** | **Visualisasi Diagram ERD Relasional MySQL (EER Model)** | 3. Screenshot Database | Gambar Diagram ERD Workbench + Catatan Relasi 1:N & Foreign Key |
| **8** | **Struktur DDL, Foreign Key Constraints & Indexing** | 3. Screenshot Database | Screenshot Editor SQL DDL + Catatan CASCADE, RESTRICT & B-Tree Index |
| **9** | **Inspeksi Tabel & Seeder Satwa di MySQL Workbench** | 3. Screenshot Database | Screenshot Result Grid Workbench (Data Satwa, Badge IUCN, Habitat) |
| **10**| **Integrasi Backend Python ke MySQL (`db.py` & PyMySQL)** | Arsitektur Integrasi | 4 Pilar Jembatan Python-MySQL + Diagram Alur Request-Response |
| **11**| **Teknologi yang Digunakan (Tech Stack)** | Spesifikasi Teknis | 3 Tier Stack (Database, Backend, Frontend) |
| **12**| **Kesimpulan & Nilai Tambah Proyek** | Penutup | 3 Card Nilai Tambah + Bar Anggota Tim Pengembang |

---

## 🎙️ Panduan Narasi & Catatan Pembicara per Slide (*Speaker Notes*)

### 🌿 Slide 1: Judul & Pembuka Presentasi
* **Poin Penting**: 
  * Sambut audiens dan dosen penguji.
  * Perkenalkan nama web: **FaunaGuard**.
  * Sampaikan bahwa web ini dibangun dengan sinergi antara **arsitektur database relasional MySQL** dan **antarmuka edukasi publik modern**.
* **Contoh Narasi Pembicara**:
  > *"Selamat pagi/siang Bapak/Ibu dan rekan-rekan sekalian. Hari ini kami mempresentasikan proyek web 'FaunaGuard: Suaka Informasi dan Edukasi Konservasi Satwa Dilindungi Kalimantan'. Proyek ini dirancang tidak hanya sebagai portal edukasi hayati Pulau Borneo, namun juga mengimplementasikan arsitektur database relasional MySQL ternormalisasi 3NF yang memiliki integritas referensial solid."*

---

### 🌳 Slide 2: Latar Belakang & Urgensi Hayati Borneo (Isi Web)
* **Poin Penting**:
  1. Hutan hujan tropis Kalimantan telah ada lebih dari 130 juta tahun (salah satu yang tertua di dunia).
  2. Ancaman deforestasi, kebakaran lahan gambut, dan perburuan liar mengancam satwa seperti Orangutan, Bekantan, Badak Kalimantan, dan Pesut Mahakam.
  3. FaunaGuard hadir sebagai media advokasi dan sistem data terstruktur.
* **Contoh Narasi Pembicara**:
  > *"Mengapa Kalimantan? Hutan Borneo menyimpan keanekaragaman satwa endemik yang sangat rentan. Sayangnya, banyak satwa ikonik kini berstatus kritis (Critically Endangered). FaunaGuard hadir menjawab kebutuhan media informasi digital yang mudah diakses masyarakat untuk menumbuhkan kepedulian pelestarian satwa liar."*

---

### 🏠 Slide 3: Struktur & Konten Utama Web FaunaGuard (Isi Web)
* **Poin Penting**:
  1. **Beranda (Home)**: Pusat wawasan edukasi publik, indikator statistik cepat (*Total Spesies, Satwa Kritis, Kawasan Konservasi*), sorotan satwa langka, dan ajakan pelestarian.
  2. **Katalog Satwa**: Direktori visual eksplorasi satwa dengan kartu interaktif, lencana status IUCN, dan sistem pencarian.
  3. **Panel Manajemen (CRUD)**: Panel kontrol untuk mengelola catatan satwa langsung ke database MySQL.

---

### ⚡ Slide 4: Fitur-Fitur di Web: Modul Publik & Edukasi (Fitur Web)
* **Poin Penting**:
  1. **Kartu Satwa Interaktif**: Rasio foto 16:9, lencana warna status IUCN (CR: Merah/Oranye Kritis, EN: Oranye, VU: Kuning), dan estimasi populasi.
  2. **Pencarian Cepat & Filter Multi-Kriteria**: Query dinamis `WHERE 1=1` yang memfilter nama, taksonomi, dan status secara simultan tanpa me-reset parameter URL.
  3. **Pop-up Modal Edukatif Asinkron (Fetch API)**: Detail satwa dimuat seketika tanpa reload halaman menggunakan Vanilla JavaScript `fetch('/api/animals/<id>')`.
  4. **Fallback Gambar Otomatis**: Proteksi `referrerpolicy="no-referrer"` dan otomatis menggunakan `placeholder.svg` jika foto eksternal terblokir.

---

### 🛠️ Slide 5: Fitur-Fitur di Web: Modul CRUD & Logika Cerdas (Fitur Web)
* **Poin Penting**:
  1. **Panel Tabel CRUD Komprehensif**: View tabular rapi tersinkron langsung ke MySQL `faunaguard_db`.
  2. **Upload Gambar Lokal & Live Preview**: Dukungan unggah file gambar (JPG, PNG, WebP) dengan sanitasi nama UUID dan pratinjau instan.
  3. **Smart URL Scraper (Ekstraksi Gambar Otomatis)**: Jika pengguna menempel link artikel web, backend otomatis membaca tag `og:image` atau `twitter:image` untuk mendapatkan link gambar terbaik.
  4. **Graceful Degradation (Setup Notice)**: Jika MySQL belum dinyalakan, web menyajikan halaman panduan visual ramah pengguna, bukan halaman error sistem 500.

---

### 🗄️ Slide 6: Arsitektur Database Relasional & Normalisasi 3NF (Database)
* **Poin Penting**:
  * Mengapa 4 tabel terpisah? Menghindari **Update Anomaly**, **Insertion Anomaly**, dan **Deletion Anomaly**.
  * 4 Tabel:
    1. `categories`: Master kelas taksonomi (Mamalia, Aves, Reptil, dll.).
    2. `conservation_statuses`: Master standar IUCN Red List lengkap dengan kode warna badge.
    3. `habitats`: Master kawasan suaka & taman nasional di Kalimantan.
    4. `animals`: Tabel transaksi utama yang menghubungkan 3 tabel master via Foreign Key.

---

### 🖼️ Slide 7: [SCREENSHOT] Visualisasi Diagram ERD Relasional MySQL (Database)
* **Poin Penting**:
  * Menampilkan gambar diagram ERD MySQL Workbench beresolusi tinggi yang terpasang di slide.
  * Tunjukkan relasi **One-to-Many ($1:N$)**:
    * 1 Kategori $\rightarrow$ Banyak Satwa (`category_id`)
    * 1 Status Konservasi $\rightarrow$ Banyak Satwa (`status_id`)
    * 1 Kawasan Habitat $\rightarrow$ Banyak Satwa (`habitat_id`)
* **Gambar Tersimpan**: `pembagian_tugas/assets_ppt/erd_diagram.png`

---

### 📑 Slide 8: [SCREENSHOT] Struktur DDL, Foreign Key Constraints & Indexing (Database)
* **Poin Penting**:
  1. **`ON UPDATE CASCADE`**: Jika ID pada tabel master berubah, ID pada tabel `animals` otomatis terbarui.
  2. **`ON DELETE RESTRICT`**: Mencegah data kategori/habitat dihapus jika masih ada satwa yang menggunakannya (mencegah *orphan records*).
  3. **B-Tree Indexing**: Indeks pada `nama_lokal`, `category_id`, `status_id`, dan `habitat_id` mengoptimalkan pencarian dan JOIN dari kompleksitas $O(N)$ ke $O(\log N)$.
* **Gambar Tersimpan**: `pembagian_tugas/assets_ppt/db_schema_ddl.png`

---

### 📊 Slide 9: [SCREENSHOT] Inspeksi Tabel & Seeder di MySQL Workbench (Database)
* **Poin Penting**:
  * Menampilkan screenshot *Result Grid* MySQL Workbench yang memperlihatkan 5 baris data satwa Kalimantan (Orangutan Kalimantan, Bekantan, Badak Kalimantan, Kucing Merah Kalimantan, Enggang Gading).
  * Membuktikan bahwa query `SELECT` menggunakan operasi `JOIN` berhasil menggabungkan data dari 4 tabel berbeda menjadi satu tampilan informasi utuh.
* **Gambar Tersimpan**: `pembagian_tugas/assets_ppt/db_data_grid.png`

---

### 🔌 Slide 10: Integrasi Backend Python ke MySQL (`db.py` & PyMySQL)
* **Poin Penting**:
  * Driver PyMySQL murni tanpa dependensi C eksternal.
  * `cursorclass=pymysql.cursors.DictCursor`: Data returned berupa Python Dictionary (`animal['nama_lokal']`).
  * Keamanan terhadap **SQL Injection** melalui *parameterized query binding* (`%s`).
  * Siklus Request-Response: Browser $\rightarrow$ Flask $\rightarrow$ PyMySQL $\rightarrow$ MySQL 8.0 InnoDB $\rightarrow$ Jinja2 HTML.

---

### 💻 Slide 11: Teknologi yang Digunakan (Tech Stack)
* **Poin Penting**:
  * **Database**: MySQL 8.0+ (InnoDB Engine, utf8mb4) + MySQL Workbench 8.0 CE.
  * **Backend**: Python 3.13 + Flask 3.0 + PyMySQL + python-dotenv.
  * **Frontend**: HTML5, Vanilla CSS3 (Borneo Palette), Bootstrap 5.3.3, Vanilla JavaScript (Fetch API).

---

### 🏆 Slide 12: Kesimpulan & Penutup
* **Poin Penting**:
  * FaunaGuard berhasil membuktikan bahwa sistem edukasi satwa dapat dibangun dengan fondasi basis data relasional yang kokoh, cepat, dan aman.
  * Kolaborasi tim 4 orang (Database, Backend, Frontend UI, Frontend CRUD) berjalan terintegrasi dan terdokumentasi rapi.

---

## 💡 Tips Presentasi
1. Buka file `.pptx` menggunakan **Microsoft PowerPoint**, **Google Slides**, atau **WPS Office**.
2. Anda dapat menampilkan demo langsung web lokal di [http://127.0.0.1:5000](http://127.0.0.1:5000) pada saat transisi antara Slide 4 dan Slide 5.
3. Tunjukkan tab **MySQL Workbench** saat berada di Slide 7, 8, dan 9 untuk membuktikan kepada penguji bahwa database benar-benar berjalan di MySQL lokal Anda.

