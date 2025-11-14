import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

    # Konfigurasi untuk Docker Compose
    DB_USER = os.environ.get("DB_USER", "flaskuser")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "flaskpwd")
    DB_HOST = os.environ.get("DB_HOST", "db-master")  # ← GANTI INI: gunakan service name
    DB_PORT = os.environ.get("DB_PORT", "5432")  # ← GANTI INI: port dalam container
    DB_NAME = os.environ.get("DB_NAME", "app_db")

    SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
