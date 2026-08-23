import csv
from database.repository import DatabaseRepository
from validator.validator_parcele import validate_all

OUTPUT_FILE = "invalid_parcels.csv"


def export_invalid_parcels():
    repo = DatabaseRepository()
    try:
        parcels = repo.get_all()
        parcel_dicts = []
        for parcel in parcels:
            parcel_dicts.append({
                column.name: getattr(parcel, column.name)
                for column in parcel.__table__.columns
            })

        reports = validate_all(parcel_dicts)
        invalid = [report for report in reports if not report["is_valid"]]

        if not invalid:
            print("Nu exista parcele invalide.")
            return

        with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["parcel_id", "missing_fields", "suspect_fields"])
            for report in invalid:
                writer.writerow([
                    report["parcel_id"],
                    ", ".join(report["missing_fields"]),
                    ", ".join(report["suspect_fields"]),
                ])

        print("Export finalizat:", OUTPUT_FILE)
    finally:
        repo.close()


if __name__ == "__main__":
    export_invalid_parcels()
