import sys
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from extractor.extractor import PDFExtractor
from validator.validator_parcele import validate_all
from config.settings import settings
from database.repository import DatabaseRepository
from database.models import PDFData

def export_to_db():
    print("🚀 Pornesc exportul in DB...")

    extractor = PDFExtractor(settings.PDF_PATH)
    parcels = extractor.extract()

    print(f"📦 {len(parcels)} parcele extrase.")

    # Validare
    reports = validate_all(parcels)

    valid_parcels = [r["normalized"] for r in reports if r["is_valid"]]
    invalid_parcels = [r for r in reports if not r["is_valid"]]

    print(f"✔ Parcele valide: {len(valid_parcels)}")
    print(f"❗ Parcele invalide: {len(invalid_parcels)} (nu vor fi inserate)")

    repo = DatabaseRepository()

    inserted = 0
    skipped = 0

    for parcel in valid_parcels:
        # Daca parcel_id exista deja → skip
        exists = repo.db.query(PDFData).filter(PDFData.parcel_id == parcel["parcel_id"]).first()
        if exists:
            skipped += 1
            continue

        repo.save_parcel(parcel)
        inserted += 1

    print("🏁 Export finalizat.")
    print(f"➕ Inserate in DB: {inserted}")
    print(f"⏭ Sarite (duplicate): {skipped}")
    print(f"❗ Invalide: {len(invalid_parcels)}")

    # Salvam invalid_parcels.json
    with open("invalid_parcels.json", "w", encoding="utf-8") as f:
        json.dump(invalid_parcels, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    export_to_db()
