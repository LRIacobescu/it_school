import sys
import os

# Adauga automat radacina proiectului in sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

import json
import csv
from extractor.extractor import PDFExtractor
from config.settings import settings


OUTPUT_JSON = "extracted_parcels.json"
OUTPUT_CSV = "extracted_parcels.csv"


def export_all_from_extractor():
    extractor = PDFExtractor(settings.PDF_PATH)
    parcels = extractor.extract()

    if not parcels:
        print("⚠ Nu s-au extras parcele din PDF.")
        return

    # JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(parcels, f, indent=4, ensure_ascii=False)

    # CSV
    keys = parcels[0].keys()
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(parcels)

    print(f"✔ Export complet: {OUTPUT_JSON} + {OUTPUT_CSV}")
    print(f"{len(parcels)} parcele au fost extrase si exportate.")


if __name__ == "__main__":
    export_all_from_extractor()
