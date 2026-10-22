"""
FaunaGuard - Modul Koneksi Database MySQL
Menggunakan driver PyMySQL dengan cursor Dictionary agar data relasional 
dapat diakses dengan nama kolom yang jelas (misal: animal['nama_lokal']).
"""

import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# Muat file konfigurasi .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "faunaguard_db")


def get_db_connection():
    """
    Membuka koneksi baru ke database MySQL.
    Mengembalikan objek koneksi PyMySQL dengan cursor DictCursor.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4",
            autocommit=True
        )
        return connection
    except pymysql.MySQLError as err:
        print(f"[ERROR] Gagal terhubung ke MySQL Database ({DB_NAME}): {err}")
        raise err


def check_database_status():
    """
    Memeriksa apakah server MySQL aktif dan database faunaguard_db sudah ada.
    Mengembalikan (is_connected: bool, message: str).
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM animals;")
            res = cursor.fetchone()
            total_animals = res['total'] if res else 0
        conn.close()
        return True, f"Terhubung ke MySQL ({DB_HOST}:{DB_PORT}/{DB_NAME}) - {total_animals} satwa tercatat."
    except Exception as e:
        return False, str(e)
