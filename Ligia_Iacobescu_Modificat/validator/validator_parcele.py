import re

REQUIRED_FIELDS = [
    "parcel_id",
    "owner_name",
    "owner_street",
    "city",
    "state",
    "prop_address_1",
    "prop_acres",
    "district_1",
    "class_value",
    "acres",
    "land",
    "impts",
    "total"
]

SUSPECT_PATTERNS = {
    "parcel_id": r"^\d{3}-\d{4}-\d{3}$",
    "state": r"^[A-Z]{2}$",
    "land": r"^\$?\d{1,3}(,\d{3})*$",
    "impts": r"^\$?\d{1,3}(,\d{3})*$",
    "total": r"^\$?\d{1,3}(,\d{3})*$",
    "class_value": r"^[A-Z]\d$",
}


def normalize_money(value):
    if not value:
        return None
    value = value.replace("$", "").replace(",", "").strip()
    try:
        return float(value)
    except:
        return None


def normalize_acres(value):
    try:
        return float(value)
    except:
        return None


def validate_parcel(parcel: dict) -> dict:
    missing = []
    suspect = []
    normalized = parcel.copy()

    # 1. Detectam campuri lipsa
    for field in REQUIRED_FIELDS:
        if parcel.get(field) in (None, "", " "):
            missing.append(field)

    # 2. Detectam campuri suspecte
    for field, pattern in SUSPECT_PATTERNS.items():
        value = parcel.get(field)
        if value and not re.match(pattern, str(value)):
            suspect.append(field)

    # 3. Normalizare valori financiare
    normalized["land"] = normalize_money(parcel.get("land"))
    normalized["impts"] = normalize_money(parcel.get("impts"))
    normalized["total"] = normalize_money(parcel.get("total"))

    # 4. Normalizare acres
    normalized["prop_acres"] = normalize_acres(parcel.get("prop_acres"))
    normalized["acres"] = normalize_acres(parcel.get("acres"))

    #nu mai verificam diferentele dintre acres si prop_acres

    return {
        "parcel_id": parcel.get("parcel_id"),
        "missing_fields": missing,
        "suspect_fields": suspect,
        "normalized": normalized,
        "is_valid": len(missing) == 0 and len(suspect) == 0
    }


def validate_all(parcels: list) -> list:
    return [validate_parcel(p) for p in parcels]
