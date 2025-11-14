import psycopg2
from config import Config

def test_connection():
    try:
        conn = psycopg2.connect(
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                host=Config.DB_HOST,
                port=Config.DB_PORT)
        print("✅ Koneksi ke PostgreSQL berhasil!")
        conn.close()
    except Exception as e:
        print("❌ Gagal terhubung ke PostgreSQL:", e)

if __name__ == "__main__":
    test_connection()
