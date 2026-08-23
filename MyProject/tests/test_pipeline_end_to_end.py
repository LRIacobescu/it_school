import os
from extractor.reader import PDFReader
from extractor.parser import PDFParser
from database.repository import DatabaseRepository
from database.session import engine
from database.models import Base
from config.settings import settings


def test_pipeline_end_to_end():
    """
    Test complet FULL: PDF → Reader → Parser → DB → Read-back.
    Verifică TOATE câmpurile parcelului.
    """

    # 0. Creăm tabelele dacă nu există
    Base.metadata.create_all(bind=engine)

    # 1. Verificăm că PDF-ul există
    assert os.path.exists(settings.PDF_PATH)

    # 2. Reader: extrage text
    reader = PDFReader(settings.PDF_PATH)
    extracted = reader.auto_extract()

    raw_text = extracted["text"]
    assert isinstance(raw_text, str)
    assert len(raw_text.strip()) > 0

    # 3. Parser: extrage toate parcelele
    parser = PDFParser(raw_text)
    parcels = parser.extract_all_parcels()

    assert isinstance(parcels, list)
    assert len(parcels) > 0

    first = parcels[0]

    # 4. Salvăm în DB
    repo = DatabaseRepository()
    ids = repo.save_many(parcels)

    saved = repo.get_by_id(ids[0])

    # 5. Verificăm TOATE câmpurile
    for field, value in first.items():
        assert getattr(saved, field) == value, f"Mismatch at field: {field}"

    # 6. Cleanup
    for pid in ids:
        repo.delete(pid)

    assert repo.get_by_id(ids[0]) is None
