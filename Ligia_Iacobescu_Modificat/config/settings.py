import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# db ul principal este PostgreSQL.
# Datele de conectare se pot schimba din .env fara sa umblam prin cod.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pdf_data_explorer")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Daca vrei poti pune direct DATABASE_URL in .env.
# Altfel o construim din setarile db de mai sus.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = (
        "postgresql+psycopg://"
        + quote_plus(DB_USER)
        + ":"
        + quote_plus(DB_PASS)
        + "@"
        + DB_HOST
        + ":"
        + DB_PORT
        + "/"
        + DB_NAME
    )

# PDF_PATH ramane pentru scripturile si testele mai vechi din proiect.
PDF_PATH = os.getenv("PDF_PATH")
if not PDF_PATH or not os.path.exists(PDF_PATH):
    PDF_PATH = os.path.join(DATA_DIR, "input.pdf")

MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))


class Settings:
    BASE_DIR = BASE_DIR
    DATA_DIR = DATA_DIR
    UPLOAD_DIR = UPLOAD_DIR
    TEMPLATES_DIR = TEMPLATES_DIR
    STATIC_DIR = STATIC_DIR
    DATABASE_URL = DATABASE_URL
    PDF_PATH = PDF_PATH
    MAX_UPLOAD_SIZE_MB = MAX_UPLOAD_SIZE_MB
    DB_HOST = DB_HOST
    DB_PORT = DB_PORT
    DB_NAME = DB_NAME
    DB_USER = DB_USER
    DB_PASS = DB_PASS


settings = Settings()
