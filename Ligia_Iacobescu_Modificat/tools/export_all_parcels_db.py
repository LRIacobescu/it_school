import csv
import json
from database.repository import DatabaseRepository

OUTPUT_CSV = "all_parcels.csv"
OUTPUT_JSON = "all_parcels.json"


def parcel_to_dict(parcel):
    return {
        column.name: getattr(parcel, column.name)
        for column in parcel.__table__.columns
    }


def export_all_parcels():
    repo = DatabaseRepository()
    try:
        parcels = repo.get_all()
        if not parcels:
            print("Nu exista parcele in baza de date.")
            return

        data = [parcel_to_dict(parcel) for parcel in parcels]

        with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False, default=str)

        fieldnames = list(data[0].keys())
        with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print("Export finalizat:", OUTPUT_CSV, "+", OUTPUT_JSON)
    finally:
        repo.close()


if __name__ == "__main__":
    export_all_parcels()
