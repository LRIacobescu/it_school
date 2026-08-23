import json
import csv
from database.repository import DatabaseRepository

OUTPUT_CSV = "all_parcels.csv"
OUTPUT_JSON = "all_parcels.json"


def export_all_parcels():
    repo = DatabaseRepository()
    parcels = repo.get_all()

    if not parcels:
        print("⚠ Nu există parcele în baza de date.")
        return

    # -----------------------------
    # EXPORT JSON
    # -----------------------------
    json_ready = [p.__dict__ for p in parcels]

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_ready, f, indent=4, ensure_ascii=False)

    # -----------------------------
    # EXPORT CSV (codul tău)
    # -----------------------------
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "id",
            "parcel_id",
            "owner_name",
            "owner_street",
            "city",
            "state",
            "prop_address_1",
            "prop_address_2",
            "section",
            "prop_acres",
            "district_1",
            "district_2",
            "district_3",
            "class_value",
            "acres",
            "land",
            "impts",
            "total",
            "created_at"
        ])

        for p in parcels:
            writer.writerow([
                p.id,
                p.parcel_id,
                p.owner_name,
                p.owner_street,
                p.city,
                p.state,
                p.prop_address_1,
                p.prop_address_2,
                p.section,
                p.prop_acres,
                p.district_1,
                p.district_2,
                p.district_3,
                p.class_value,
                p.acres,
                p.land,
                p.impts,
                p.total,
                p.created_at
            ])

    print(f"✔ Export finalizat: {OUTPUT_CSV} + {OUTPUT_JSON}")
    print(f"{len(parcels)} parcele au fost exportate.")


if __name__ == "__main__":
    export_all_parcels()
