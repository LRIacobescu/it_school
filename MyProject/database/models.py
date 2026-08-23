from sqlalchemy import Column, Integer, String, Float
from database import Base

class PDFData(Base):
    __tablename__ = "pdf_data"

    id = Column(Integer, primary_key=True, index=True)

    parcel_id = Column(String, index=True)
    owner_name = Column(String)
    owner_street = Column(String)

    city = Column(String)
    state = Column(String)
    zip_code = Column(String)   # <-- NOUA COLOANĂ

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
