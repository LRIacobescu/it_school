import os
from extractor.reader import PDFReader
from config.settings import settings


def test_reader_auto_extract():
    """
    Test complet pentru PDFReader:
    - verifică existența PDF-ului
    - verifică extragerea textului
    - verifică detectarea tipului PDF-ului
    """

    # 1. PDF-ul trebuie să existe
    assert os.path.exists(settings.PDF_PATH), f"Fișierul PDF nu există: {settings.PDF_PATH}"

    # 2. Reader-ul trebuie să poată fi instanțiat
    reader = PDFReader(settings.PDF_PATH)

    # 3. Extragerea trebuie să returneze un dict cu 'text' și 'type'
    result = reader.auto_extract()

    assert isinstance(result, dict)
    assert "text" in result
    assert "type" in result

    # 4. Tipul PDF-ului trebuie să fie valid
    assert result["type"] in ["digital", "scanat"]

    # 5. Textul extras trebuie să fie non-gol
    text = result["text"]
    assert isinstance(text, str)
    assert len(text.strip()) > 0

    # 6. Textul trebuie să conțină cel puțin un pattern recognoscibil
    # (ex: un parcel_id)
    import re
    has_parcel_id = bool(re.search(r"\d{3}-\d{4}-\d{3}", text))
    assert has_parcel_id, "Reader-ul a extras text, dar nu a detectat niciun parcel_id."
