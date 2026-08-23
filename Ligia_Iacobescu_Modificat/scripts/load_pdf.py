from extractor.extractor import PDFExtractor
from database.repository import DatabaseRepository
from database import Base, engine
from config.settings import settings


def run_pipeline():
    print("Pornire pipeline PDF -> DB")
    Base.metadata.create_all(bind=engine)

    parcels = PDFExtractor(settings.PDF_PATH).extract()
    print("Numar parcele detectate:", len(parcels))

    repo = DatabaseRepository()
    try:
        ids = repo.save_many(parcels)
        print(str(len(ids)) + " parcele salvate in baza de date.")
    finally:
        repo.close()


if __name__ == "__main__":
    run_pipeline()
