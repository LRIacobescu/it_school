import os
import tempfile
import pytest
from extractor.reader import PDFReader
from config.settings import PDF_PATH


# ---------------------------------------------------------
# Helper: creează un PDFReader rapid (fără OCR)
# ---------------------------------------------------------
def create_reader():
    return PDFReader(PDF_PATH)


# ---------------------------------------------------------
# 1. Test: structura rezultatului auto_extract()
# ---------------------------------------------------------
def test_reader_auto_extract_structure():
    reader = create_reader()
    result = reader.auto_extract()

    assert isinstance(result, dict)
    assert "type" in result
    assert "text" in result
    assert "tables" in result

    assert isinstance(result["text"], str)
    assert isinstance(result["tables"], list)


# ---------------------------------------------------------
# 2. Test: tipul PDF-ului trebuie să fie digital
# ---------------------------------------------------------
def test_reader_detects_digital_pdf():
    reader = create_reader()
    result = reader.auto_extract()

    assert result["type"] == "digital"


# ---------------------------------------------------------
# 3. Test: textul extras nu trebuie să fie gol
# ---------------------------------------------------------
def test_reader_extract_text_not_empty():
    reader = create_reader()
    result = reader.auto_extract()

    assert len(result["text"].strip()) > 0


# ---------------------------------------------------------
# 4. Test: tabelele trebuie să fie listă de liste
# ---------------------------------------------------------
def test_reader_extract_tables_structure():
    reader = create_reader()
    result = reader.auto_extract()

    assert "tables" in result
    assert isinstance(result["tables"], list)

    if result["tables"]:
        first_table = result["tables"][0]
        assert isinstance(first_table, list), "Tabelul trebuie să fie listă"
        assert isinstance(first_table[0], list), "Rândurile tabelului trebuie să fie liste"


# ---------------------------------------------------------
# 5. Test: reader-ul trebuie să funcționeze pe primele pagini
# ---------------------------------------------------------
def test_reader_partial_processing():
    reader = create_reader()
    result = reader.auto_extract()

    # verificăm doar primele caractere, nu tot PDF-ul
    assert result["text"][:50].strip() != ""


# ---------------------------------------------------------
# 6. Test: reader-ul nu trebuie să arunce excepții
# ---------------------------------------------------------
def test_reader_no_exceptions():
    reader = create_reader()
    result = reader.auto_extract()

    assert isinstance(result, dict)


# ---------------------------------------------------------
# 7. Test: fișier invalid → trebuie să arunce excepție
# ---------------------------------------------------------
def test_reader_invalid_file():
    # creăm un fișier temporar invalid
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"%PDF-INVALID-DATA")
        invalid_path = tmp.name

    reader = PDFReader(invalid_path)

    with pytest.raises(Exception):
        reader.auto_extract()

    os.remove(invalid_path)


# ---------------------------------------------------------
# 8. Test: reader-ul trebuie să aibă metodele necesare
# ---------------------------------------------------------
def test_reader_methods_exist():
    reader = create_reader()

    assert hasattr(reader, "extract_text")
    assert hasattr(reader, "extract_tables")
    assert hasattr(reader, "auto_extract")
