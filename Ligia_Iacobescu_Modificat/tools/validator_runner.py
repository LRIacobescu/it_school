import json
import sys
import os

# Asiguram ca MyProject/ este in sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from extractor.extractor import PDFExtractor
from validator.validator_parcele import validate_all
from config.settings import settings


def run_validator():
    print("🔍 Rulez validatorul universal...")

    extractor = PDFExtractor(settings.PDF_PATH)
    parcels = extractor.extract()

    print(f"📦 {len(parcels)} parcele extrase. Validez...")

    reports = validate_all(parcels)
    invalid = [r for r in reports if not r["is_valid"]]

    with open("invalid_parcels.json", "w", encoding="utf-8") as f:
        json.dump(invalid, f, indent=4, ensure_ascii=False)

    print(f"✔ Validator finalizat.")
    print(f"❗ Parcele invalide: {len(invalid)}")
    print("📁 Raport salvat in invalid_parcels.json")


if __name__ == "__main__":
    run_validator()
