import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from database.session import engine, Base
from database.models import PDFData

print("📐 Creez tabelele în PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Tabele create cu succes!")