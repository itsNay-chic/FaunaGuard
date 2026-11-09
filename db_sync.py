"""
FaunaGuard - Modul Sinkronisasi Otomatis Database MySQL ke File SQL & GitHub.
Setiap kali data satwa ditambah, diubah, atau dihapus melalui aplikasi web,
modul ini otomatis:
1. Mengekspor isi database MySQL faunaguard_db terkini ke database/faunaguard_schema.sql
2. Melakukan commit & push ke repositori GitHub origin main secara otomatis di latar belakang (background thread).
"""

import os
import subprocess
import threading
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "faunaguard_db")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SCHEMA_SQL_PATH = os.path.join(BASE_DIR, "database", "faunaguard_schema.sql")


def sql_format_value(val):
    """Memformat nilai Python menjadi format SQL yang aman dan valid."""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    # Escape backslash dan single quote untuk SQL
    escaped = str(val).replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


def export_database_to_sql(output_path=None):
    """
    Mengekspor seluruh tabel dan data aktif dari MySQL faunaguard_db
    menjadi file SQL lengkap di database/faunaguard_schema.sql.
    """
    if not output_path:
        output_path = SCHEMA_SQL_PATH

    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4"
    )

    try:
        with conn.cursor() as cursor:
            # Ambil data dari 4 tabel utama
            cursor.execute("SELECT * FROM categories ORDER BY id ASC;")
            categories = cursor.fetchall()

            cursor.execute("SELECT * FROM conservation_statuses ORDER BY id ASC;")
            statuses = cursor.fetchall()

            cursor.execute("SELECT * FROM habitats ORDER BY id ASC;")
            habitats = cursor.fetchall()

            cursor.execute("SELECT * FROM animals ORDER BY id ASC;")
            animals = cursor.fetchall()

        lines = [
            "-- =============================================================================",
            "-- FaunaGuard: Database Relasional MySQL Konservasi Satwa Dilindungi Kalimantan",
            "-- File ini diperbarui secara OTOMATIS saat data diubah melalui aplikasi web.",
            "-- =============================================================================",
            "",
            "CREATE DATABASE IF NOT EXISTS faunaguard_db ",
            "    CHARACTER SET utf8mb4 ",
            "    COLLATE utf8mb4_unicode_ci;",
            "",
            "USE faunaguard_db;",
            "",
            "SET FOREIGN_KEY_CHECKS = 0;",
            "DROP TABLE IF EXISTS animals;",
            "DROP TABLE IF EXISTS habitats;",
            "DROP TABLE IF EXISTS conservation_statuses;",
            "DROP TABLE IF EXISTS categories;",
            "SET FOREIGN_KEY_CHECKS = 1;",
            "",
            "CREATE TABLE categories (",
            "    id INT AUTO_INCREMENT PRIMARY KEY,",
            "    nama_kategori VARCHAR(50) NOT NULL UNIQUE,",
            "    deskripsi TEXT NULL",
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
            "",
            "CREATE TABLE conservation_statuses (",
            "    id INT AUTO_INCREMENT PRIMARY KEY,",
            "    kode VARCHAR(10) NOT NULL UNIQUE,",
            "    nama_status VARCHAR(50) NOT NULL,",
            "    warna_badge VARCHAR(20) DEFAULT '#D98327',",
            "    tingkat_ancaman VARCHAR(50) NOT NULL",
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
            "",
            "CREATE TABLE habitats (",
            "    id INT AUTO_INCREMENT PRIMARY KEY,",
            "    nama_habitat VARCHAR(100) NOT NULL,",
            "    lokasi VARCHAR(100) NOT NULL,",
            "    tipe_ekosistem VARCHAR(50) NOT NULL",
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
            "",
            "CREATE TABLE animals (",
            "    id INT AUTO_INCREMENT PRIMARY KEY,",
            "    nama_lokal VARCHAR(100) NOT NULL,",
            "    nama_ilmiah VARCHAR(100) NOT NULL,",
            "    deskripsi TEXT NULL,",
            "    ancaman_utama TEXT NULL,",
            "    estimasi_populasi INT NULL,",
            "    category_id INT NOT NULL,",
            "    status_id INT NOT NULL,",
            "    habitat_id INT NOT NULL,",
            "    foto_url MEDIUMTEXT NULL,",
            "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,",
            "    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,",
            "  ",
            "    CONSTRAINT fk_animal_category ",
            "        FOREIGN KEY (category_id) REFERENCES categories (id) ",
            "        ON UPDATE CASCADE ON DELETE RESTRICT,",
            "        ",
            "    CONSTRAINT fk_animal_status ",
            "        FOREIGN KEY (status_id) REFERENCES conservation_statuses (id) ",
            "        ON UPDATE CASCADE ON DELETE RESTRICT,",
            "        ",
            "    CONSTRAINT fk_animal_habitat ",
            "        FOREIGN KEY (habitat_id) REFERENCES habitats (id) ",
            "        ON UPDATE CASCADE ON DELETE RESTRICT",
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
            "",
            "CREATE INDEX idx_animals_nama ON animals (nama_lokal);",
            "CREATE INDEX idx_animals_category ON animals (category_id);",
            "CREATE INDEX idx_animals_status ON animals (status_id);",
            "CREATE INDEX idx_animals_habitat ON animals (habitat_id);",
            ""
        ]

        # 1. Categories seeder
        if categories:
            lines.append("INSERT INTO categories (id, nama_kategori, deskripsi) VALUES")
            cat_rows = []
            for c in categories:
                cat_rows.append(f"({c['id']}, {sql_format_value(c['nama_kategori'])}, {sql_format_value(c['deskripsi'])})")
            lines.append(",\n".join(cat_rows) + ";\n")

        # 2. Conservation statuses seeder
        if statuses:
            lines.append("INSERT INTO conservation_statuses (id, kode, nama_status, warna_badge, tingkat_ancaman) VALUES")
            stat_rows = []
            for s in statuses:
                stat_rows.append(
                    f"({s['id']}, {sql_format_value(s['kode'])}, {sql_format_value(s['nama_status'])}, "
                    f"{sql_format_value(s['warna_badge'])}, {sql_format_value(s['tingkat_ancaman'])})"
                )
            lines.append(",\n".join(stat_rows) + ";\n")

        # 3. Habitats seeder
        if habitats:
            lines.append("INSERT INTO habitats (id, nama_habitat, lokasi, tipe_ekosistem) VALUES")
            hab_rows = []
            for h in habitats:
                hab_rows.append(
                    f"({h['id']}, {sql_format_value(h['nama_habitat'])}, {sql_format_value(h['lokasi'])}, "
                    f"{sql_format_value(h['tipe_ekosistem'])})"
                )
            lines.append(",\n".join(hab_rows) + ";\n")

        # 4. Animals seeder
        if animals:
            lines.append("INSERT INTO animals (")
            lines.append("    id, nama_lokal, nama_ilmiah, deskripsi, ancaman_utama,")
            lines.append("    estimasi_populasi, category_id, status_id, habitat_id, foto_url")
            lines.append(") VALUES")
            animal_rows = []
            for a in animals:
                row_str = (
                    f"(\n"
                    f"    {a['id']},\n"
                    f"    {sql_format_value(a['nama_lokal'])},\n"
                    f"    {sql_format_value(a['nama_ilmiah'])},\n"
                    f"    {sql_format_value(a['deskripsi'])},\n"
                    f"    {sql_format_value(a['ancaman_utama'])},\n"
                    f"    {sql_format_value(a['estimasi_populasi'])},\n"
                    f"    {a['category_id']},\n"
                    f"    {a['status_id']},\n"
                    f"    {a['habitat_id']},\n"
                    f"    {sql_format_value(a['foto_url'])}\n"
                    f")"
                )
                animal_rows.append(row_str)
            lines.append(",\n".join(animal_rows) + ";\n")

        # Query verifikasi akhir
        lines.extend([
            "SELECT ",
            "    a.id,",
            "    a.nama_lokal,",
            "    a.nama_ilmiah,",
            "    c.nama_kategori,",
            "    s.kode AS status_iucn,",
            "    s.nama_status,",
            "    s.tingkat_ancaman,",
            "    h.nama_habitat,",
            "    h.lokasi AS habitat_lokasi,",
            "    a.estimasi_populasi,",
            "    a.ancaman_utama",
            "FROM animals a",
            "JOIN categories c ON a.category_id = c.id",
            "JOIN conservation_statuses s ON a.status_id = s.id",
            "JOIN habitats h ON a.habitat_id = h.id",
            "ORDER BY a.id ASC;",
            ""
        ])

        sql_content = "\n".join(lines)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sql_content)

        print(f"[FaunaGuard Sync] Berhasil mengekspor database ({len(animals)} satwa) ke {output_path}")
        return True, f"Berhasil mengekspor {len(animals)} satwa ke {output_path}"
    except Exception as e:
        print(f"[FaunaGuard Sync ERROR] Gagal mengekspor database: {e}")
        return False, str(e)
    finally:
        conn.close()


def _git_push_worker(commit_message):
    """Worker background thread untuk git add, commit, dan push ke origin main."""
    try:
        # 1. git add schema file & uploads directory
        subprocess.run(
            ["git", "add", "database/faunaguard_schema.sql"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=15
        )
        if os.path.exists(os.path.join(BASE_DIR, "static", "uploads")):
            subprocess.run(
                ["git", "add", "static/uploads"],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                timeout=15
            )

        # 2. git commit
        res_commit = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=15
        )

        output_str = (res_commit.stdout or "") + (res_commit.stderr or "")
        if "nothing to commit" in output_str.lower():
            print("[FaunaGuard Sync] Tidak ada perubahan baru untuk di-commit ke GitHub.")
            return

        # 3. git push ke origin main
        res_push = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if res_push.returncode == 0:
            print(f"[FaunaGuard Sync] Sinkronisasi GitHub BERHASIL: {commit_message}")
        else:
            print(f"[FaunaGuard Sync Warning] Git push exit code {res_push.returncode}: {res_push.stderr}")
    except Exception as err:
        print(f"[FaunaGuard Sync Warning] Background Git push error: {err}")


def sync_database_to_github(commit_message="chore(db): sinkronisasi otomatis database ke github", background=True):
    """
    Ekspor data aktif MySQL ke faunaguard_schema.sql lalu push ke GitHub.
    Jika background=True, git push dijalankan di thread terpisah agar UI web tetap cepat.
    """
    # 1. Ekspor file SQL secara sinkron (sangat cepat, < 20ms)
    ok, msg = export_database_to_sql()
    if not ok:
        return False, msg

    # 2. Push ke GitHub
    if background:
        thread = threading.Thread(target=_git_push_worker, args=(commit_message,), daemon=True)
        thread.start()
        return True, "Ekspor SQL selesai & git push berjalan di latar belakang."
    else:
        _git_push_worker(commit_message)
        return True, "Ekspor SQL dan git push selesai."
