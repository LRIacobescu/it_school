from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship
from database import Base


class PDFData(Base):
    """Modelul vechi de parcele, pastrat pentru compatibilitate cu scripturile initiale."""

    __tablename__ = "pdf_data"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(String, index=True)
    owner_name = Column(String)
    owner_street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    prop_address_1 = Column(String)
    prop_address_2 = Column(String)
    section = Column(String)
    prop_acres = Column(Float)
    district_1 = Column(String)
    district_2 = Column(String)
    district_3 = Column(String)
    class_value = Column(String)
    acres = Column(Float)
    land = Column(String)
    impts = Column(String)
    total = Column(String)


class UploadedDocument(Base):
    """Un PDF incarcat prin interfata web."""

    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    column_metadata = Column(JSON, nullable=False, default=list)
    extraction_mode = Column(String, nullable=False, default="table")

    rows = relationship(
        "DocumentRow",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DocumentRow(Base):
    """Un rand din tabelul extras. JSON permite coloane dinamice pentru orice PDF."""

    __tablename__ = "document_rows"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("uploaded_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    row_number = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)

    document = relationship("UploadedDocument", back_populates="rows")
