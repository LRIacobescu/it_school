import os
import re
from extractor.extractor import PDFExtractor
from config.settings import settings


def test_extractor_full_pipeline():
    """
    Test complet pentru PDFExtractor:
    - verifică extragerea textului
    - verifică extragerea parcelelor
    - verifică TOATE câmpurile din fiecare parcel
    """

    # 1. PDF-ul trebuie să existe
    assert os.path.exists(settings.PDF_PATH), f"Fișierul PDF nu există: {settings.PDF_PATH}"

    # 2. Instanțiem extractorul
    extractor = PDFExtractor(settings.PDF_PATH)

    # 3. Rulăm pipeline-ul complet
    parcels = extractor.extract()

    # 4. Extractorul trebuie să returneze o listă
    assert isinstance(parcels, list)
    assert len(parcels) > 0

    parcel = parcels[0]

    # 5. Toate câmpurile trebuie să existe
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

    # 6. Câmpuri critice trebuie să fie non-goale
    assert parcel["parcel_id"]
    assert parcel["owner_name"]
    assert parcel["city"]
    assert parcel["state"]

    # 7. Pattern parcel_id
    assert re.match(r"\d{3}-\d{4}-\d{3}", parcel["parcel_id"])

    # 8. State trebuie să fie două litere
    assert re.match(r"^[A-Z]{2}$", parcel["state"])

    # 9. Valori numerice
    assert isinstance(parcel["prop_acres"], float)
    assert isinstance(parcel["acres"], float)

    # 10. Valori monetare
    assert parcel["land"].startswith("$")
    assert parcel["total"].startswith("$")
