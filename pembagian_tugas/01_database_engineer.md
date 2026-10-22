# 📘 Panduan Tugas Anggota 1: Database Engineer & Data Architect

## 👤 Identitas Peran
- **Nama Peran**: Database Engineer & Data Architect (Perancang & Pengelola Basis Data)
- **Tanggung Jawab**: Merancang skema relasional database, memastikan integritas data (Normalisasi 3NF & Foreign Key), membuat script DDL & Seeder SQL, serta membangun modul koneksi database Python (`db.py`).
- **File Kerja Utama**:
  1. [`database/faunaguard_schema.sql`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/database/faunaguard_schema.sql)
  2. [`db.py`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/db.py)
  3. [`.env`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/.env) dan [`.env.example`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/.env.example)

---

## 🏗️ 1. Pemahaman Arsitektur Basis Data (ERD & Normalisasi)

### Mengapa Database Dibuat 4 Tabel (Normalisasi 3NF)?
Jika data satwa hanya disimpan dalam 1 tabel raksasa (*flat table*), akan terjadi **Redundansi Data** dan **Anomali**:
- **Update Anomaly**: Jika status IUCN "Critically Endangered" ingin diubah namanya, kita harus mengubah ratusan baris satwa satu per satu.
- **Insertion Anomaly**: Kita tidak bisa menambahkan data habitat baru sebelum ada satwa yang tercatat di habitat tersebut.
- **Deletion Anomaly**: Jika satwa terakhir di suatu habitat dihapus, informasi habitat tersebut ikut terhapus permanen.

Oleh karena itu, dibuat 4 tabel terpisah yang saling berelasi:
```
┌──────────────────────┐         ┌────────────────────────┐
│      categories      │         │ conservation_statuses  │
├──────────────────────┤         ├────────────────────────┤
│ PK  id               │         │ PK  id                 │
│     nama_kategori    │         │     kode               │
│     deskripsi        │         │     nama_status        │
└──────────┬───────────┘         │     warna_badge        │
           │ 1                   │     tingkat_ancaman    │
           │                     └───────────┬────────────┘
           │ N                               │ 1
           │       ┌─────────────────┐       │
           └──────►│     animals     │◄──────┘
                   ├─────────────────┤ N
                   │ PK  id          │
                   │     nama_lokal  │
                   │     nama_ilmiah │
                   │     deskripsi   │
                   │     foto_url    │
                   │ FK  category_id │
                   │ FK  status_id   │
                   │ FK  habitat_id  │
                   └────────▲────────┘
                            │ N
                            │ 1
                   ┌────────┴────────┐
                   │    habitats     │
                   ├─────────────────┤
                   │ PK  id          │
                   │     nama_habitat│
                   │     lokasi      │
                   │     tipe_ekosistem
                   └─────────────────┘
```

### Penjelasan Tabel:
1. **`categories`** (Master Data): Menyimpan kelompok taksonomi ilmiah (Mamalia, Aves, Reptilia).
2. **`conservation_statuses`** (Master Data): Standar status kepunahan global IUCN Red List (CR, EN, VU) lengkap dengan kode hex warna untuk antarmuka web.
3. **`habitats`** (Master Data Dinamis): Kawasan konservasi alami Kalimantan (misal: *Taman Nasional Tanjung Puting*, *DAS Mahakam*).
4. **`animals`** (Tabel Transaksi Utama): Menyimpan data satwa individu yang menghubungkan ketiga tabel master melalui Foreign Key.

---

## 🔑 2. Fitur Kunci & Kode yang Wajib Dipahami

### A. Integritas Referensial & Foreign Key (`faunaguard_schema.sql`)
Lihat baris [faunaguard_schema.sql:L70-L81](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/database/faunaguard_schema.sql#L70-L81):
```sql
CONSTRAINT fk_animal_category 
    FOREIGN KEY (category_id) REFERENCES categories (id) 
    ON UPDATE CASCADE ON DELETE RESTRICT,
    
CONSTRAINT fk_animal_status 
    FOREIGN KEY (status_id) REFERENCES conservation_statuses (id) 
    ON UPDATE CASCADE ON DELETE RESTRICT,
    
CONSTRAINT fk_animal_habitat 
    FOREIGN KEY (habitat_id) REFERENCES habitats (id) 
    ON UPDATE CASCADE ON DELETE RESTRICT
```
- **`ON UPDATE CASCADE`**: Jika ID master berubah, ID pada tabel `animals` otomatis ikut berubah.
- **`ON DELETE RESTRICT`**: Mencegah penghapusan habitat atau kategori yang masih dipakai oleh satwa, sehingga database terlindungi dari data yatim (*orphan records*).

### B. Indexing Database untuk Akses Cepat
Lihat baris [faunaguard_schema.sql:L84-L87](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/database/faunaguard_schema.sql#L84-L87):
```sql
CREATE INDEX idx_animals_nama ON animals (nama_lokal);
CREATE INDEX idx_animals_category ON animals (category_id);
CREATE INDEX idx_animals_status ON animals (status_id);
CREATE INDEX idx_animals_habitat ON animals (habitat_id);
```
- Digunakan untuk mempercepat proses pencarian (*WHERE nama_lokal LIKE...*) dan operasi penggabungan (*JOIN*) dari kompleksitas $O(N)$ menjadi $O(\log N)$ menggunakan struktur B-Tree.

### C. Jembatan Koneksi Python ke MySQL (`db.py`)
Lihat baris [db.py:L22-L42](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/db.py#L22-L42):
- Menggunakan driver murni Python **`pymysql`** tanpa ketergantungan library C compiler eksternal.
- Mengaktifkan **`cursorclass=pymysql.cursors.DictCursor`**: Agar hasil query database dikembalikan berupa Python Dictionary (`animal['nama_lokal']`), bukan tuple angka (`animal[1]`), sehingga kode backend jauh lebih mudah dibaca dan dipelihara.
- Menggunakan `autocommit=True` agar setiap eksekusi INSERT/UPDATE/DELETE langsung tersimpan permanen ke MySQL tanpa perlu memanggil `conn.commit()` manual setiap saat.

---

## 🎤 3. Simulasi Pertanyaan Dosen & Kunci Jawaban (Q&A)

### Q1: Mengapa tidak memakai SQLite saja yang lebih sederhana?
> **Jawaban**:  
> "Kami sengaja menggunakan **MySQL 8.0** karena proyek FaunaGuard dirancang dengan standar arsitektur relasional tingkat produksi (*production-grade*). MySQL memiliki fitur *concurrency* yang jauh lebih baik untuk aplikasi multi-user, dukungan tipe data `utf8mb4` untuk karakter internasional, indexing B-Tree yang optimal, serta integrasi langsung dengan perangkat lunak visual standar industri seperti **MySQL Workbench**."

### Q2: Apa fungsi `DictCursor` pada file `db.py`?
> **Jawaban**:  
> "Secara default, driver database mengembalikan baris sebagai *tuple* indeks numerik (misal: `row[0]`, `row[1]`). Dengan `DictCursor`, PyMySQL mengembalikan data dalam bentuk *dictionary key-value* (misal: `row['nama_lokal']`, `row['foto_url']`). Hal ini sangat mempermudah pengolahan data di backend Flask dan rendering pada template HTML Jinja2."

### Q3: Bagaimana cara memastikan database tetap aman jika kredensial diunggah ke GitHub?
> **Jawaban**:  
> "Kami menerapkan standar *12-Factor App* dengan memisahkan kredensial database ke dalam file `.env` yang tidak boleh di-commit ke Git (`.gitignore`). Kami hanya menyediakan file `.env.example` sebagai template konfigurasi untuk pengembang lain."
