"""
FaunaGuard - Portal Informasi Satwa Dilindungi Kalimantan
Aplikasi Web Backend Menggunakan Flask & PyMySQL.
Fokus: Arsitektur Database Relasional MySQL & Media Edukasi Publik.
"""

import os
import re
import uuid
import urllib.request
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import get_db_connection, DB_NAME, DB_HOST, DB_PORT

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "faunaguard-secret-key-borneo-2026")

# Konfigurasi Upload File Gambar
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Maksimum 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_direct_image_url(url):
    """
    Jika pengguna memasukkan URL halaman web/artikel berita (bukan link langsung file gambar),
    fungsi ini otomatis mengekstrak Open Graph Image (og:image) atau twitter:image dari metadata halaman.
    """
    if not url:
        return url
    url = url.strip()

    # Jika sudah berformat file gambar langsung atau path internal
    lower_clean = url.lower().split("?")[0]
    if lower_clean.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg")) or url.startswith("/static/"):
        return url

    # Jika berupa URL web (http/https)
    if url.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                }
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                content_type = response.headers.get("Content-Type", "")
                if "image" in content_type:
                    return url

                # Baca bagian awal HTML untuk mencari tag meta og:image
                raw_html = response.read(150000).decode("utf-8", errors="ignore")

                match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', raw_html, re.I)
                if not match:
                    match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', raw_html, re.I)
                if not match:
                    match = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', raw_html, re.I)
                if not match:
                    match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']', raw_html, re.I)

                if match:
                    extracted = match.group(1).strip()
                    if extracted.startswith("//"):
                        return "https:" + extracted
                    elif extracted.startswith("/"):
                        parsed = urlparse(url)
                        return f"{parsed.scheme}://{parsed.netloc}{extracted}"
                    return extracted
        except Exception as e:
            print(f"[FaunaGuard Info] Info ekstrasi gambar dari URL {url}: {e}")

    return url



@app.errorhandler(Exception)
def handle_database_error(error):
    """
    Menangkap kegagalan koneksi database secara anggun (graceful degradation)
    dan menyajikan panduan setup visual jika database belum diaktifkan di MySQL Workbench.
    """
    error_str = str(error)
    if "Can't connect to MySQL" in error_str or "Unknown database" in error_str or "Access denied" in error_str:
        return render_template(
            "setup_notice.html",
            error_message=error_str,
            db_name=DB_NAME,
            db_host=DB_HOST,
            db_port=DB_PORT
        ), 500
    raise error


# =============================================================================
# 1. RUTE PUBLIK: Media Penyebaran Informasi & Edukasi
# =============================================================================

@app.route("/")
def index():
    """
    Halaman Utama (Public Information Portal)
    Menampilkan Hero Konservasi, Statistik Cepat, Filter Interaktif,
    serta Kartu Informasi Satwa (Animal Cards).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Ambil Data Kategori & Status untuk Filter
            cursor.execute("SELECT * FROM categories ORDER BY nama_kategori ASC;")
            categories = cursor.fetchall()

            cursor.execute("SELECT * FROM conservation_statuses ORDER BY id ASC;")
            statuses = cursor.fetchall()

            # 2. Hitung Statistik Konservasi untuk Banner Edukasi
            cursor.execute("SELECT COUNT(*) AS total_spesies FROM animals;")
            stat_total = cursor.fetchone()["total_spesies"]

            cursor.execute("""
                SELECT COUNT(*) AS total_kritis 
                FROM animals a 
                JOIN conservation_statuses s ON a.status_id = s.id 
                WHERE s.kode = 'CR';
            """)
            stat_kritis = cursor.fetchone()["total_kritis"]

            cursor.execute("SELECT COUNT(DISTINCT habitat_id) AS total_habitat FROM animals;")
            stat_habitat = cursor.fetchone()["total_habitat"]

            # 3. Parameter Pencarian & Filter dari URL
            q = request.args.get("q", "").strip()
            cat_filter = request.args.get("category", "").strip()
            status_filter = request.args.get("status", "").strip()

            # 4. Konstruksi Query Relasional dengan Filter Dinamis
            query = """
                SELECT 
                    a.id,
                    a.nama_lokal,
                    a.nama_ilmiah,
                    a.deskripsi,
                    a.ancaman_utama,
                    a.estimasi_populasi,
                    a.foto_url,
                    a.created_at,
                    c.id AS category_id,
                    c.nama_kategori,
                    s.id AS status_id,
                    s.kode AS status_kode,
                    s.nama_status,
                    s.warna_badge,
                    s.tingkat_ancaman,
                    h.id AS habitat_id,
                    h.nama_habitat,
                    h.lokasi AS habitat_lokasi,
                    h.tipe_ekosistem
                FROM animals a
                JOIN categories c ON a.category_id = c.id
                JOIN conservation_statuses s ON a.status_id = s.id
                JOIN habitats h ON a.habitat_id = h.id
                WHERE 1=1
            """
            params = []

            if q:
                query += " AND (a.nama_lokal LIKE %s OR a.nama_ilmiah LIKE %s OR a.deskripsi LIKE %s)"
                params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])

            if cat_filter and cat_filter.isdigit():
                query += " AND a.category_id = %s"
                params.append(int(cat_filter))

            if status_filter and status_filter.isdigit():
                query += " AND a.status_id = %s"
                params.append(int(status_filter))

            query += " ORDER BY a.id ASC;"

            cursor.execute(query, params)
            animals = cursor.fetchall()

        return render_template(
            "index.html",
            animals=animals,
            categories=categories,
            statuses=statuses,
            stats={
                "total": stat_total,
                "kritis": stat_kritis,
                "habitat": stat_habitat
            },
            current_q=q,
            current_category=cat_filter,
            current_status=status_filter
        )
    finally:
        conn.close()


@app.route("/api/animals/<int:animal_id>")
def get_animal_detail(animal_id):
    """
    API endpoint untuk mengambil detail satwa dalam format JSON 
    guna memuat informasi mendalam pada pop-up modal edukasi.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.*,
                    c.nama_kategori,
                    s.kode AS status_kode,
                    s.nama_status,
                    s.warna_badge,
                    s.tingkat_ancaman,
                    h.nama_habitat,
                    h.lokasi AS habitat_lokasi,
                    h.tipe_ekosistem
                FROM animals a
                JOIN categories c ON a.category_id = c.id
                JOIN conservation_statuses s ON a.status_id = s.id
                JOIN habitats h ON a.habitat_id = h.id
                WHERE a.id = %s;
            """, (animal_id,))
            animal = cursor.fetchone()

        if not animal:
            return jsonify({"error": "Satwa tidak ditemukan"}), 404

        return jsonify(animal)
    finally:
        conn.close()


# =============================================================================
# 2. RUTE PENGELOLAAN DATA: Panel CRUD untuk Admin/Pengelola
# =============================================================================

@app.route("/manage")
def manage():
    """
    Halaman Tabel Kelola Data Satwa (Read View untuk Admin).
    Menampilkan data terelasi secara tabular lengkap dengan tombol Aksi (Edit & Hapus).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.nama_lokal,
                    a.nama_ilmiah,
                    a.estimasi_populasi,
                    a.foto_url,
                    c.nama_kategori,
                    s.kode AS status_kode,
                    s.nama_status,
                    s.warna_badge,
                    h.nama_habitat
                FROM animals a
                JOIN categories c ON a.category_id = c.id
                JOIN conservation_statuses s ON a.status_id = s.id
                JOIN habitats h ON a.habitat_id = h.id
                ORDER BY a.id ASC;
            """)
            animals = cursor.fetchall()

        return render_template("manage.html", animals=animals)
    finally:
        conn.close()


@app.route("/animals/add", methods=["GET", "POST"])
def add_animal():
    """
    Fitur Create: Tambah Data Satwa Baru.
    Mendukung upload file gambar langsung dari komputer atau tautan URL gambar.
    """
    conn = get_db_connection()
    try:
        if request.method == "POST":
            nama_lokal = request.form.get("nama_lokal", "").strip()
            nama_ilmiah = request.form.get("nama_ilmiah", "").strip()
            deskripsi = request.form.get("deskripsi", "").strip()
            ancaman_utama = request.form.get("ancaman_utama", "").strip()
            populasi_str = request.form.get("estimasi_populasi", "").strip()
            category_id = request.form.get("category_id")
            status_id = request.form.get("status_id")
            habitat_id = request.form.get("habitat_id")
            foto_url = request.form.get("foto_url", "").strip()

            estimasi_populasi = int(populasi_str) if populasi_str.isdigit() else None

            # 1. Cek apakah ada file yang diunggah
            uploaded_file = request.files.get("foto_file")
            if uploaded_file and uploaded_file.filename and allowed_file(uploaded_file.filename):
                safe_name = secure_filename(uploaded_file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                save_dest = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
                uploaded_file.save(save_dest)
                foto_url = f"/static/uploads/{unique_filename}"
            elif foto_url:
                # 2. Jika input berupa URL, pastikan diekstrak jika itu tautan artikel web
                foto_url = extract_direct_image_url(foto_url)

            # Validasi kolom wajib
            if not nama_lokal or not nama_ilmiah or not category_id or not status_id or not habitat_id:
                flash("Harap lengkapi seluruh kolom wajib bertanda bintang (*).", "danger")
                return redirect(url_for("add_animal"))

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO animals (
                        nama_lokal, nama_ilmiah, deskripsi, ancaman_utama, 
                        estimasi_populasi, category_id, status_id, habitat_id, foto_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    nama_lokal, nama_ilmiah, deskripsi, ancaman_utama,
                    estimasi_populasi, category_id, status_id, habitat_id, foto_url
                ))

            flash(f"Data satwa '{nama_lokal}' berhasil ditambahkan ke database!", "success")
            return redirect(url_for("manage"))

        # GET request: ambil data referensi foreign key untuk form
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM categories ORDER BY nama_kategori ASC;")
            categories = cursor.fetchall()

            cursor.execute("SELECT * FROM conservation_statuses ORDER BY id ASC;")
            statuses = cursor.fetchall()

            cursor.execute("SELECT * FROM habitats ORDER BY nama_habitat ASC;")
            habitats = cursor.fetchall()

        return render_template(
            "add_animal.html",
            categories=categories,
            statuses=statuses,
            habitats=habitats
        )
    finally:
        conn.close()


@app.route("/animals/edit/<int:animal_id>", methods=["GET", "POST"])
def edit_animal(animal_id):
    """
    Fitur Update: Mengubah Data Satwa yang Sudah Tersimpan.
    Mendukung pengisian kawasan habitat secara manual (nama habitat, lokasi, ekosistem)
    serta upload foto baru atau URL foto.
    """
    conn = get_db_connection()
    try:
        if request.method == "POST":
            nama_lokal = request.form.get("nama_lokal", "").strip()
            nama_ilmiah = request.form.get("nama_ilmiah", "").strip()
            deskripsi = request.form.get("deskripsi", "").strip()
            ancaman_utama = request.form.get("ancaman_utama", "").strip()
            populasi_str = request.form.get("estimasi_populasi", "").strip()
            category_id = request.form.get("category_id")
            status_id = request.form.get("status_id")
            habitat_id = request.form.get("habitat_id")
            nama_habitat = request.form.get("nama_habitat", "").strip()
            habitat_lokasi = request.form.get("habitat_lokasi", "").strip()
            tipe_ekosistem = request.form.get("tipe_ekosistem", "").strip()
            foto_url = request.form.get("foto_url", "").strip()

            estimasi_populasi = int(populasi_str) if populasi_str.isdigit() else None

            # 1. Resolusi Kawasan Habitat (Manual Input)
            if nama_habitat:
                if not habitat_lokasi:
                    habitat_lokasi = "Kalimantan"
                if not tipe_ekosistem:
                    tipe_ekosistem = "Hutan Tropis Kalimantan"

                with conn.cursor() as cursor:
                    # Cari apakah kawasan habitat dengan nama ini sudah ada
                    cursor.execute(
                        "SELECT id FROM habitats WHERE LOWER(TRIM(nama_habitat)) = LOWER(TRIM(%s)) LIMIT 1;",
                        (nama_habitat,)
                    )
                    existing_h = cursor.fetchone()
                    if existing_h:
                        habitat_id = existing_h["id"]
                        # Perbarui informasi lokasi dan tipe ekosistem jika diubah
                        cursor.execute("""
                            UPDATE habitats 
                            SET lokasi = %s, tipe_ekosistem = %s 
                            WHERE id = %s;
                        """, (habitat_lokasi, tipe_ekosistem, habitat_id))
                    else:
                        # Tambahkan kawasan habitat baru ke tabel habitats
                        cursor.execute("""
                            INSERT INTO habitats (nama_habitat, lokasi, tipe_ekosistem)
                            VALUES (%s, %s, %s);
                        """, (nama_habitat, habitat_lokasi, tipe_ekosistem))
                        habitat_id = cursor.lastrowid

            # Validasi kolom wajib
            if not nama_lokal or not nama_ilmiah or not category_id or not status_id or not habitat_id:
                flash("Harap lengkapi kolom wajib (*), termasuk informasi Kawasan Habitat.", "danger")
                return redirect(url_for("edit_animal", animal_id=animal_id))

            # 2. Ambil foto satwa yang saat ini tersimpan di DB
            with conn.cursor() as cursor:
                cursor.execute("SELECT foto_url FROM animals WHERE id = %s;", (animal_id,))
                current_data = cursor.fetchone()
                existing_foto = current_data["foto_url"] if current_data else ""

            # Periksa apakah ada file gambar baru yang diunggah
            uploaded_file = request.files.get("foto_file")
            if uploaded_file and uploaded_file.filename and allowed_file(uploaded_file.filename):
                safe_name = secure_filename(uploaded_file.filename)
                unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                save_dest = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
                uploaded_file.save(save_dest)
                final_foto_url = f"/static/uploads/{unique_filename}"
            elif foto_url:
                # Jika user memasukkan URL baru
                final_foto_url = extract_direct_image_url(foto_url)
            else:
                # Pertahankan foto yang sudah ada jika tidak diisi/diunggah ulang
                final_foto_url = existing_foto

            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE animals SET
                        nama_lokal = %s,
                        nama_ilmiah = %s,
                        deskripsi = %s,
                        ancaman_utama = %s,
                        estimasi_populasi = %s,
                        category_id = %s,
                        status_id = %s,
                        habitat_id = %s,
                        foto_url = %s
                    WHERE id = %s;
                """, (
                    nama_lokal, nama_ilmiah, deskripsi, ancaman_utama,
                    estimasi_populasi, category_id, status_id, habitat_id, final_foto_url,
                    animal_id
                ))

            flash(f"Data satwa '{nama_lokal}' berhasil diperbarui!", "success")
            return redirect(url_for("manage"))

        # GET request: ambil satwa target berserta data habitat relasinya
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.*,
                    h.nama_habitat,
                    h.lokasi AS habitat_lokasi,
                    h.tipe_ekosistem
                FROM animals a
                LEFT JOIN habitats h ON a.habitat_id = h.id
                WHERE a.id = %s;
            """, (animal_id,))
            animal = cursor.fetchone()

            if not animal:
                flash("Data satwa tidak ditemukan.", "danger")
                return redirect(url_for("manage"))

            cursor.execute("SELECT * FROM categories ORDER BY nama_kategori ASC;")
            categories = cursor.fetchall()

            cursor.execute("SELECT * FROM conservation_statuses ORDER BY id ASC;")
            statuses = cursor.fetchall()

            cursor.execute("SELECT * FROM habitats ORDER BY nama_habitat ASC;")
            habitats = cursor.fetchall()

        return render_template(
            "edit_animal.html",
            animal=animal,
            categories=categories,
            statuses=statuses,
            habitats=habitats
        )
    finally:
        conn.close()


@app.route("/animals/delete/<int:animal_id>", methods=["POST"])
def delete_animal(animal_id):
    """
    Fitur Delete: Hapus Data Satwa dari Database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nama_lokal FROM animals WHERE id = %s;", (animal_id,))
            animal = cursor.fetchone()
            nama = animal["nama_lokal"] if animal else f"ID {animal_id}"

            cursor.execute("DELETE FROM animals WHERE id = %s;", (animal_id,))

        flash(f"Data satwa '{nama}' berhasil dihapus dari database.", "info")
        return redirect(url_for("manage"))
    finally:
        conn.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    print("\n=======================================================")
    print(" 🌿 FaunaGuard: Suaka Informasi Satwa Kalimantan")
    print(f" Database Target: MySQL ({DB_HOST}:{DB_PORT}/{DB_NAME})")
    print(f" Web Server Berjalan di: http://127.0.0.1:{port}")
    print("=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=debug)
