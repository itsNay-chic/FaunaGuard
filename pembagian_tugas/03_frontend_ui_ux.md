# 📙 Panduan Tugas Anggota 3: Frontend Developer (UI/UX & Public Portal)

## 👤 Identitas Peran
- **Nama Peran**: Frontend Developer — UI/UX & Public Information Portal
- **Tanggung Jawab**: Merancang identitas visual web bertema Hutan Tropis Kalimantan, membangun master layout (`base.html`), menyusun halaman beranda informasi publik (`index.html`), menerapkan sistem filter interaktif, memastikan responsivitas perangkat seluler (*mobile-friendly*), serta mengatasi isu pemblokiran gambar eksternal.
- **File Kerja Utama**:
  1. [`templates/base.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/base.html)
  2. [`templates/index.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/index.html)
  3. [`templates/setup_notice.html`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/setup_notice.html)
  4. [`static/css/style.css`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/css/style.css)
  5. [`static/img/placeholder.svg`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/img/placeholder.svg)

---

## 🎨 1. Konsep Desain & Sistem Token Visual Borneo Rainforest

Aplikasi FaunaGuard dibangun dengan estetika modern khas hutan Kalimantan menggunakan variabel CSS (*Design Tokens*):

| Variabel CSS | Kode Warna | Filosofi & Kegunaan |
|---|---|---|
| `--fg-primary` | `#186049` | *Deep Rainforest Emerald* — Melambangkan kelebatan kanopi hutan tropis Borneo. Digunakan pada Navbar, Header, dan Elemen Kunci. |
| `--fg-secondary` | `#24785c` | *Borneo Forest Green* — Digunakan untuk elemen pendukung dan kartu statistik. |
| `--fg-accent` | `#4a943e` | *Fresh Moss Green* — Digunakan untuk ikon habitat dan lencana kategori satwa. |
| `--fg-amber` | `#d98327` | *Borneo Orangutan Amber* — Melambangkan warna bulu Orangutan Kalimantan. Digunakan pada tombol aksi utama (*Call to Action*) dan status kritis. |
| `--fg-cream` | `#ece8af` | *Warm Sandstone Cream* — Warna aksen hangat untuk teks kontras dan background aksen. |

Lihat implementasi token pada baris [style.css:L1-L20](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/css/style.css#L1-L20).

---

## 🔑 2. Fitur Kunci & Kode yang Wajib Dipahami

### A. Master Layout & Templating Jinja2 (`base.html`)
Lihat baris [base.html:L1-L35](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/base.html#L1-L35):
- **Prinsip DRY (*Don't Repeat Yourself*)**: Seluruh header, navbar, footer, dan import CDN Bootstrap 5 didefinisikan satu kali di `base.html`. Halaman lain tinggal melakukan `{% extends "base.html" %}`.
- **Navigasi Aktif Otomatis**: Kelas navbar otomatis menjadi `active` berdasarkan request URL endpoint menggunakan sintaks Jinja2:
  ```html
  class="nav-link {% if request.endpoint == 'index' %}active{% endif %}"
  ```
- **Sistem Notifikasi Flash**: Pesan sukses atau error dari backend langsung ditampilkan secara otomatis menggunakan Bootstrap Dismissible Alert pada baris [base.html:L53-L64](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/base.html#L53-L64).

### B. Mencegah Pemblokiran Hotlink Gambar (`no-referrer`)
Lihat baris [base.html:L5](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/templates/base.html#L5):
```html
<meta name="referrer" content="no-referrer">
```
- **Masalah Nyata di Web**: Server gambar besar (seperti Wikimedia Commons, Flickr, atau portal berita) sering memblokir gambar dengan pesan **HTTP 403 Forbidden** jika browser mengirimkan header referer lokal (`http://127.0.0.1:5000/`).
- **Solusi**: Tag `<meta name="referrer" content="no-referrer">` memerintahkan browser untuk tidak mengirimkan header asal, sehingga gambar dari manapun dapat dimuat tanpa terblokir.

### C. Halaman Beranda Publik Edukasi (`index.html`)
1. **Hero Banner & Call to Action**: Menyajikan pesan konservasi mendalam tentang pentingnya menjaga kelestarian satwa endemik Kalimantan.
2. **Statistik Cepat Konservasi**: Menampilkan 3 kartu ringkasan data yang dihitung secara dinamis dari database (Total Satwa, Satwa Kritis CR, dan Kawasan Konservasi).
3. **Filter Pencarian Multi-Kriteria**: Formulir pencarian instan yang menggabungkan input teks (*Search Box*), dropdown kategori taksonomi, dan status IUCN. Filter mempertahankan nilai input sebelumnya melalui parameter URL (`current_q`, `current_category`, `current_status`).
4. **Grid Kartu Satwa Modern**:
   - Dilengkapi *status badge overlay* dengan warna latar belakang yang diambil langsung dari database (`style="background-color: {{ animal.warna_badge }};"`).
   - Efek *hover micro-interaction* pada kartu satwa (`transform: translateY(-6px)` dan bayangan lembut) yang membuat aplikasi terasa hidup.

### D. Aset Cadangan Vektor SVG Mandiri (`placeholder.svg`)
Lihat file [`static/img/placeholder.svg`](file:///c:/Users/ASUS/.gemini/antigravity/scratch/faunaguard/static/img/placeholder.svg):
- Dibuat menggunakan format SVG murni dengan grafis siluet hutan Borneo dan lencana pelindung satwa.
- Pada setiap elemen `<img>`, disematkan penanganan fallback:
  ```html
  onerror="this.onerror=null; this.src='{{ url_for('static', filename='img/placeholder.svg') }}';"
  ```
- **Keunggulan**: Jika URL foto satwa suatu saat terhapus dari internet atau saat laptop sedang *offline*, web tidak akan menampilkan ikon gambar rusak yang jelek, melainkan menampilkan ilustrasi vektor resmi FaunaGuard.

---

## 🎤 3. Simulasi Pertanyaan Dosen & Kunci Jawaban (Q&A)

### Q1: Mengapa gambar dari internet terkadang tidak muncul di localhost dan bagaimana cara Anda mengatasinya?
> **Jawaban**:  
> "Hal tersebut disebabkan oleh kebijakan *Hotlink Protection* pada server penyedia gambar (seperti Wikimedia Commons) yang memeriksa header HTTP `Referer`. Jika referer berasal dari `localhost` atau domain asing, server menolaknya dengan error 403. Kami mengatasinya dengan menyematkan tag `<meta name="referrer" content="no-referrer">` pada `base.html` dan atribut `referrerpolicy="no-referrer"` pada setiap tag gambar."

### Q2: Bagaimana cara Anda memastikan web tetap responsif di layar HP dan monitor besar?
> **Jawaban**:  
> "Kami memanfaatkan sistem *12-Column Responsive Grid* Bootstrap 5 dipadukan dengan *CSS Flexbox*. Pada grid katalog satwa, kami menggunakan kelas `row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4` sehingga tampilan otomatis menyesuaikan: 1 kolom di layar ponsel, 2 kolom di tablet, dan 3 kolom di layar desktop."

### Q3: Mengapa tidak memakai framework Tailwind CSS saja?
> **Jawaban**:  
> "Kami memilih kombinasi Bootstrap 5 CDN dan **Vanilla CSS kustom** agar memiliki kontrol penuh atas *design tokens* palet warna hutan Borneo tanpa menimbulkan *overhead bundle* kompilasi Node.js/PostCSS. Hal ini membuat aplikasi sangat ringan, memuat cepat, dan mudah dipelajari secara arsitektural."
