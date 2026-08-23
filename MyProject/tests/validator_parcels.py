import re

REQUIRED_FIELDS = [
    "parcel_id",
    "owner_name",
    "owner_street",
    "city",
    "state",
    "prop_address_1",
    "prop_address_2",
    "prop_acres",
    "district_1",
    "district_2",
    "district_3",
    "class_value",
    "acres",
    "land",
    "impts",
    "total"
]

SUSPECT_PATTERNS = {
    "parcel_id": r"^\d{3}-\d{4}-\d{3}$",
    "state": r"^[A-Z]{2}$",
    "land": r"^\$\d{1,3}(,\d{3})*$",
    "impts": r"^\$\d{1,3}(,\d{3})*$",
    "total": r"^\$\d{1,3}(,\d{3})*$",
    "class_value": r"^[A-Z]\d$"
}


def validate_parcel(parcel: dict) -> dict:
    """
    Returnează un raport de validare pentru un singur parcel.
    """

    missing = []
    suspect = []

    # 1. Detectăm câmpurile lipsă
    for field in REQUIRED_FIELDS:
        if field not in parcel or parcel[field] in (None, "", " "):
            missing.append(field)

    # 2. Detectăm câmpurile suspecte (pattern invalid)
    for field, pattern in SUSPECT_PATTERNS.items():
        value = parcel.get(field)
        if value and not re.match(pattern, str(value)):
            suspect.append(field)

    # 3. Detectăm valori numerice suspecte
    if parcel.get("prop_acres") == 0:
        suspect.append("prop_acres")

    if parcel.get("acres") == 0:
        suspect.append("acres")

    return {
        "parcel_id": parcel.get("parcel_id"),
        "missing_fields": missing,
        "suspect_fields": suspect,
        "is_valid": len(missing) == 0 and len(suspect) == 0
    }


def validate_all(parcels: list) -> list:
    """
    Rulează validatorul pe toate parcelele.
    """
    return [validate_parcel(p) for p in parcels]


def print_validation_report(reports: list):
    """
    Afișează raportul în terminal, colorat.
    """

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    for report in reports:
        print(f"\n{CYAN}Parcel {report['parcel_id']}{RESET}")

        if report["is_valid"]:
            print(f"{GREEN}✔ Parcel valid{RESET}")
        else:
            print(f"{YELLOW}⚠ Parcel invalid{RESET}")

        if report["missing_fields"]:
            print(f"{RED}Missing: {', '.join(report['missing_fields'])}{RESET}")

        if report["suspect_fields"]:
            print(f"{YELLOW}Suspect: {', '.join(report['suspect_fields'])}{RESET}")
