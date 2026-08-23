import os
from dotenv import load_dotenv

# Încarcă variabilele din .env dacă există
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# PDF PATH – dacă nu ai PDF_PATH în .env, folosește fallback-ul

PDF_PATH = os.getenv(
    "PDF_PATH",
    os.path.join(BASE_DIR, "data", "input.pdf")  # fallback dacă nu ai .env (ascunde parolele si permite configurare flexibila - e obligatoriu daca ai proiecte mari)
)


# DATABASE CONFIG

# DATABASE CONFIG – toate valorile vin din .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

class Settings:
    BASE_DIR = BASE_DIR
    PDF_PATH = PDF_PATH
    DB_HOST = DB_HOST
    DB_PORT = DB_PORT
    DB_NAME = DB_NAME
    DB_USER = DB_USER
    DB_PASS = DB_PASS
    DATABASE_URL = DATABASE_URL

settings = Settings()