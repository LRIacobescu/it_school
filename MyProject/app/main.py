from extractor.reader import PDFReader
from extractor.parser import PDFParser
from database.repository import DatabaseRepository
from database.session import engine
from database.models import Base
from config.settings import settings


def run_pipeline():
    print("Pornire pipeline PDF → DB")

    # 0. Creăm tabelele dacă nu există
    Base.metadata.create_all(bind=engine)

    # 1. Extragere PDF
    reader = PDFReader(settings.PDF_PATH)
    extracted = reader.auto_extract()

    print(f"Tip PDF detectat: {extracted['type']}")
    print("Text extras...")

    raw_text = extracted["text"]

    # 2. Parsare text (extrage toate parcelele)
    parser = PDFParser(raw_text)
    parcels = parser.extract_all_parcels()

    print(f"Număr parcele detectate: {len(parcels)}")

    # 3. Salvare în PostgreSQL
    repo = DatabaseRepository()
    ids = repo.save_many(parcels)

    print(f"{len(ids)} parcele salvate în baza de date.")
    print("Pipeline finalizat")


if __name__ == "__main__":
    run_pipeline()
