# 📕 Panduan Tugas Anggota 4: Frontend Developer (CRUD Panel & Interaktivitas JS)

## 👤 Identitas Peran
- **Nama Peran**: Frontend Developer — CRUD Panel & Client-side Interaction
- **Tanggung Jawab**: Membangun panel pengelolaan data admin (`manage.html`), formulir Tambah Satwa (`add_animal.html`), formulir Edit Satwa (`edit_animal.html`), serta menulis script interaktivitas JavaScript sisi klien (`main.js`) untuk pratinjau foto langsung, input habitat manual, dan modal edukasi asinkron (AJAX / Fetch API).
- **File Kerja Utama**:
  1. [`templates/manage.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/manage.html)
  2. [`templates/add_animal.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/add_animal.html)
  3. [`templates/edit_animal.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/edit_animal.html)
  4. [`static/js/main.js`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/js/main.js)

---

## 💻 1. Pemahaman Panel CRUD & Interaktivitas Sisi Klien

Tugas utama Anggota 4 adalah memastikan pengalaman pengguna (*User Experience / UX*) pada operasi **CRUD (Create, Read, Update, Delete)** berjalan mulus, intuitif, dan responsif tanpa hambatan teknis.

```mermaid
graph LR
    subgraph Sisi Klien (Browser)
        M[Tombol Detail Satwa] -->|Event show.bs.modal| JS[Script main.js]
        JS -->|fetch /api/animals/:id| API[Endpoint Flask API]
        F1[Pilih File Gambar] -->|URL.createObjectURL| Prev[Kotak Live Preview]
        F2[Ketik Nama Habitat] -->|Event input datalist| AutoFill[Auto-fill Lokasi & Ekosistem]
        DelBtn[Tombol Hapus] -->|confirmDelete| Confirm{Konfirmasi Dialog}
    end
    
    subgraph Sisi Server
        API -->|JSON Response| JS
        Confirm -->|Ya| PostDel[POST /animals/delete/:id]
    end
```

---

## 🔑 2. Fitur Kunci & Kode yang Wajib Dipahami

### A. Tabel Kelola Data Admin (`manage.html`)
Lihat baris [manage.html:L30-L100](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/manage.html#L30-L100):
- **Tampilan Terelasi Tabular**: Menyajikan data satwa lengkap yang sudah di-JOIN dengan tabel kategori, status IUCN, dan habitat.
- **Thumbnail Foto Satwa**: Dilengkapi atribut `referrerpolicy="no-referrer"` dan fallback SVG otomatis jika link gambar rusak.
- **Konfirmasi Hapus Aman**: Menggunakan event `onsubmit="return confirmDelete('{{ a.nama_lokal }}');"` untuk mencegah admin menghapus data satwa secara tidak sengaja.

### B. Pratinjau Gambar Langsung (*Live Image Preview*)
Lihat baris [add_animal.html:L183-L238](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/add_animal.html#L183-L238):
- **Pilihan 1 (Upload File Lokal)**:
  Saat pengguna memilih foto dari laptop/HP, JavaScript membaca file di memori menggunakan API modern browser:
  ```javascript
  const objectUrl = URL.createObjectURL(file);
  previewImg.src = objectUrl;
  previewStatus.textContent = `✓ File siap: ${file.name} (${Math.round(file.size / 1024)} KB)`;
  ```
  Pengguna bisa langsung melihat fotonya **sebelum** menekan tombol Simpan!
- **Pilihan 2 (Link URL Gambar)**:
  Saat pengguna mengetik/menempelkan link URL, event `load` dan `error` pada elemen gambar memverifikasi secara langsung:
  - Jika link valid: Status berubah hijau `"✓ Gambar valid dan berhasil dimuat"`.
  - Jika link rusak atau berupa artikel web: Status berubah merah memperingatkan pengguna untuk menyalin *"Alamat Gambar"* (*Copy image address*).

### C. Input Kawasan Habitat Manual & Rekomendasi Pintar (`edit_animal.html`)
Lihat baris [edit_animal.html:L82-L170](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/edit_animal.html#L82-L170) dan [edit_animal.html:L315-L337](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/edit_animal.html#L315-L337):
- **Bebas Input Manual**: Tidak lagi dibatasi dropdown 5 habitat bawaan. Pengguna dapat mengetik kawasan baru apa pun (misal: *Hutan Lindung Wehea*, *Taman Nasional Sebangau*).
- **Auto-fill Pintar dari Datalist**:
  Disediakan objek lookup JavaScript berisi data habitat yang sudah tersimpan:
  ```javascript
  const knownHabitats = {
      {% for h in habitats %}
      "{{ h.nama_habitat }}": { lokasi: "{{ h.lokasi }}", ekosistem: "{{ h.tipe_ekosistem }}" },
      {% endfor %}
  };
  ```
  Jika pengguna mengetik/memilih nama yang cocok dengan habitat terdaftar, kolom **Lokasi** dan **Tipe Ekosistem** otomatis terisi, namun **tetap bisa diedit bebas** oleh pengguna.

### D. Modal Pop-up Edukasi Asinkron (`main.js`)
Lihat baris [main.js:L9-L71](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/js/main.js#L9-L71):
- **Pemuatan Cepat Tanpa Reload Halaman (Fetch API)**:
  Saat tombol *"Pelajari Selengkapnya"* pada kartu satwa diklik:
  1. Event listener mendeteksi tombol dan mengambil atribut `data-animal-id`.
  2. Mengirim request asinkron ke server: `await fetch('/api/animals/' + animalId)`.
  3. Mengubah DOM modal (judul, nama latin, status IUCN, deskripsi peran ekologis, ancaman kepunahan, estimasi populasi, dan foto besar) secara instan.

---

## 🎤 3. Simulasi Pertanyaan Dosen & Kunci Jawaban (Q&A)

### Q1: Bagaimana cara kerja Live Preview saat pengguna memilih file gambar dari komputernya?
> **Jawaban**:  
> "Kami menggunakan Web API standar browser yaitu `URL.createObjectURL(file)`. Metode ini membuat representasi string URL sementara yang mengarah langsung ke objek file di memori browser pengguna, tanpa perlu mengunggah file ke server terlebih dahulu. Hal ini sangat hemat bandwidth dan memberikan *instant feedback* kepada pengguna."

### Q2: Mengapa pada form Edit Satwa, Kawasan Habitat diubah menjadi input manual? Bukankah dropdown lebih mudah?
> **Jawaban**:  
> "Dropdown statis memiliki kelemahan besar (*rigid*): jika ada satwa baru dari kawasan konservasi yang belum ada di database, admin tidak bisa menyimpannya. Dengan input teks manual yang dipadukan tag `<datalist>` dan mapping JavaScript, admin mendapatkan fleksibilitas maksimal: dapat memilih kawasan yang sudah ada dengan fitur *autofill*, sekaligus leluasa mengetik kawasan konservasi baru yang langsung diproses secara dinamis oleh backend."

### Q3: Mengapa tombol hapus data satwa dibungkus dalam tag `<form method="POST">`, bukan link biasa `<a>`?
> **Jawaban**:  
> "Sesuai dengan standar keamanan arsitektur REST dan HTTP, operasi yang mengubah kondisi data di server (*state-changing action*) seperti DELETE atau UPDATE tidak boleh menggunakan metode `GET` (link biasa). Jika menggunakan link `GET`, web crawler atau prefetching browser bisa secara tidak sengaja memicu penghapusan data. Oleh karena itu, tombol hapus wajib dibungkus dalam form dengan metode `POST` dan dilindungi konfirmasi konfirmasi JavaScript."
