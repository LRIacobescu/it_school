import re
from extractor.parser import PDFParser


def test_parser_extract_all_parcels():
    """
    Test complet pentru PDFParser:
    - verifică extragerea tuturor parcelelor
    - verifică TOATE câmpurile din fiecare parcel
    - verifică pattern-uri critice (parcel_id, state, valori numerice)
    """

    raw_text = """
    540-1389-000
    DENNIS R LINZMEYER
    3515 S PENNSYLVANIA AVE
    SAINT FRANCIS WI
    3515 S PENNSYLVANIA AVE
    SECTION 33
    Acres: 0.12
    District 1: SAINT FRANCIS SCHOOL DISTRICT
    District 2: MILWAUKEE COUNTY
    District 3: -
    Class: G1
    Acres Total: 0.12
    Land: $18,100
    Impts: $0
    Total: $18,100
    """

    parser = PDFParser(raw_text)
    parcels = parser.extract_all_parcels()

    # 1. Parserul trebuie să returneze o listă
    assert isinstance(parcels, list)
    assert len(parcels) > 0

    parcel = parcels[0]

    # 2. Toate câmpurile trebuie să existe
    expected_fields = [
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
        "total"
    ]

    for field in expected_fields:
        assert field in parcel, f"Missing field: {field}"

    # 3. Câmpuri critice trebuie să fie non-goale
    assert parcel["parcel_id"]
    assert parcel["owner_name"]
    assert parcel["city"]
    assert parcel["state"]

    # 4. Pattern parcel_id
    assert re.match(r"\d{3}-\d{4}-\d{3}", parcel["parcel_id"])

    # 5. State trebuie să fie două litere
    assert re.match(r"^[A-Z]{2}$", parcel["state"])

    # 6. Valori numerice
    assert isinstance(parcel["prop_acres"], float)
    assert isinstance(parcel["acres"], float)

    # 7. Valori monetare
    assert parcel["land"].startswith("$")
    assert parcel["total"].startswith("$")
