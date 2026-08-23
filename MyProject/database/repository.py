from database.models import PDFData
from database.session import SessionLocal

class DatabaseRepository:
    def __init__(self):
        self.db = SessionLocal()

    def save_parcel(self, parcel_data: dict):
        """
        Salvează un singur parcel în baza de date.
        parcel_data este dict-ul returnat de parser.
        """

        # Filtrăm doar câmpurile care există în modelul PDFData
        allowed_fields = {
            "parcel_id",
            "owner_name",
            "owner_street",
            "city",
            "state",
            "zip_code",          # <-- NOUA COLOANĂ
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
        }

        filtered_data = {k: v for k, v in parcel_data.items() if k in allowed_fields}

        pdf_data = PDFData(**filtered_data)

        self.db.add(pdf_data)
        self.db.commit()
        self.db.refresh(pdf_data)

        return pdf_data.id

    def save_many(self, parcels: list):
        """
        Salvează o listă de parcele.
        """

        ids = []

        allowed_fields = {
            "parcel_id",
            "owner_name",
            "owner_street",
            "city",
            "state",
            "zip_code",          # <-- NOUA COLOANĂ
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
        }

        for parcel in parcels:
            filtered_data = {k: v for k, v in parcel.items() if k in allowed_fields}

            pdf_data = PDFData(**filtered_data)
            self.db.add(pdf_data)
            self.db.commit()
            self.db.refresh(pdf_data)
            ids.append(pdf_data.id)

        return ids

    def get_all(self):
        return self.db.query(PDFData).all()

    def get_by_id(self, parcel_id: int):
        return self.db.query(PDFData).filter(PDFData.id == parcel_id).first()

    def delete(self, parcel_id: int):
        obj = self.get_by_id(parcel_id)
        if not obj:
            return False

        self.db.delete(obj)
        self.db.commit()
        return True
