import os
from config.settings import settings
from extractor.reader import PDFReader


def test_pdf_path_is_valid():
    """
    Verifică că PDF_PATH este valid, există și poate fi citit de PDFReader.
    """

    # 1. Path-ul trebuie să existe
    assert os.path.exists(settings.PDF_PATH), f"Fișierul PDF nu există: {settings.PDF_PATH}"

    # 2. Trebuie să fie un fișier PDF
    assert settings.PDF_PATH.lower().endswith(".pdf"), "PDF_PATH nu indică un fișier .pdf"

    # 3. Reader-ul trebuie să poată deschide fișierul
    reader = PDFReader(settings.PDF_PATH)
    result = reader.auto_extract()

    # 4. Extragerea trebuie să returneze text
    assert "text" in result
    assert isinstance(result["text"], str)
    assert len(result["text"].strip()) > 0

    # 5. Tipul PDF-ului trebuie să fie detectat corect
    assert result["type"] in ["digital", "scanat"]
