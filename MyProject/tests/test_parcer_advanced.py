import pytest
from extractor.parser import PDFParser


def test_clean_text_removes_extra_spaces():
    raw = "Nume:   Ligia\n\n\nOraș:   Deva"
    parser = PDFParser(raw)
    cleaned = parser.clean_text()

    assert "  " not in cleaned, "Parser-ul nu a eliminat spațiile multiple"
    assert cleaned.count("\n") < raw.count("\n"), "Parser-ul nu a eliminat liniile goale"


def test_clean_text_handles_special_characters():
    raw = "Nume: Ligia © ® ™\nAdresă: Str. Principală"
    parser = PDFParser(raw)
    cleaned = parser.clean_text()

    assert "©" not in cleaned
    assert "®" not in cleaned
    assert "™" not in cleaned


def test_extract_key_values_basic():
    raw = """
    Nume: Ligia
    Oraș: Deva
    Vârstă: 30
    """
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    assert metadata["Nume"] == "Ligia"
    assert metadata["Oraș"] == "Deva"
    assert metadata["Vârstă"] == "30"


def test_extract_key_values_no_metadata():
    raw = "Acesta este un text fără metadata."
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    assert isinstance(metadata, dict)
    assert len(metadata) == 0, "Parser-ul ar trebui să returneze dict gol"


def test_extract_key_values_duplicate_keys():
    raw = """
    Nume: Ligia
    Nume: Maria
    """
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    # ultimul câștigă
    assert metadata["Nume"] == "Maria"


def test_extract_key_values_handles_colon_in_value():
    raw = """
    Descriere: Acesta este un text: cu două puncte.
    """
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    assert metadata["Descriere"] == "Acesta este un text: cu două puncte."


def test_clean_text_long_input():
    raw = "Nume: Ligia\n" * 5000  # text foarte lung
    parser = PDFParser(raw)
    cleaned = parser.clean_text()

    assert len(cleaned) > 0
    assert cleaned.count("Nume") == 5000


def test_extract_key_values_mixed_format():
    raw = """
    Nume : Ligia
    Oraș:Deva
    Vârstă :30
    Email: ligia@example.com
    """
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    assert metadata["Nume"] == "Ligia"
    assert metadata["Oraș"] == "Deva"
    assert metadata["Vârstă"] == "30"
    assert metadata["Email"] == "ligia@example.com"


def test_extract_key_values_ignores_invalid_lines():
    raw = """
    Nume: Ligia
    Aceasta nu este o linie validă
    Oraș: Deva
    """
    parser = PDFParser(raw)
    metadata = parser.extract_key_values()

    assert "Aceasta nu este o linie validă" not in metadata
    assert metadata["Nume"] == "Ligia"
    assert metadata["Oraș"] == "Deva"
