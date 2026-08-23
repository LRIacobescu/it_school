import csv
from database.repository import DatabaseRepository
from validator_parcels import validate_all


OUTPUT_FILE = "invalid_parcels.csv"


def export_invalid_parcels():
    repo = DatabaseRepository()

    # 1. Luăm toate parcelele din DB
    parcels = repo.get_all()

    # 2. Validăm toate parcelele
    reports = validate_all([p.__dict__ for p in parcels])

    # 3. Filtrăm doar parcelele invalide
    invalid = [r for r in reports if not r["is_valid"]]

    if not invalid:
        print("✔ Nu există parcele invalide. CSV nu a fost generat.")
        return

    # 4. Export CSV
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # header
        writer.writerow([
            "parcel_id",
            "missing_fields",
            "suspect_fields"
        ])

        # rows
        for r in invalid:
            writer.writerow([
                r["parcel_id"],
                ", ".join(r["missing_fields"]),
                ", ".join(r["suspect_fields"])
            ])

    print(f"⚠ Export finalizat: {OUTPUT_FILE}")
    print(f"{len(invalid)} parcele invalide au fost exportate.")


if __name__ == "__main__":
    export_invalid_parcels()
