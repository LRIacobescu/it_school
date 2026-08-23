from database.models import DocumentRow, PDFData, UploadedDocument
from database.session import SessionLocal


class DatabaseRepository:
    def __init__(self, db=None):
        self.db = db or SessionLocal()
        self._owns_session = db is None

    def close(self):
        if self._owns_session:
            self.db.close()

    # ------------------------------------------------------------------
    # CRUD vechi - pastrat si reparat
    # ------------------------------------------------------------------
    def _legacy_allowed_fields(self):
        return {
            "parcel_id", "owner_name", "owner_street", "city", "state", "zip_code",
            "prop_address_1", "prop_address_2", "section", "prop_acres",
            "district_1", "district_2", "district_3", "class_value",
            "acres", "land", "impts", "total"
        }

    def save_parcel(self, parcel_data):
        filtered = {
            key: value for key, value in parcel_data.items()
            if key in self._legacy_allowed_fields()
        }
        obj = PDFData(**filtered)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj.id

    def save_many(self, parcels):
        objects = []
        allowed = self._legacy_allowed_fields()
        for parcel in parcels:
            filtered = {key: value for key, value in parcel.items() if key in allowed}
            objects.append(PDFData(**filtered))

        self.db.add_all(objects)
        self.db.commit()
        for obj in objects:
            self.db.refresh(obj)
        return [obj.id for obj in objects]

    def get_all(self):
        return self.db.query(PDFData).all()

    def get_by_id(self, parcel_id):
        return self.db.query(PDFData).filter(PDFData.id == parcel_id).first()

    def update(self, parcel_id, changes):
        obj = self.get_by_id(parcel_id)
        if not obj:
            return False

        allowed = self._legacy_allowed_fields()
        for key, value in changes.items():
            if key in allowed:
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return True

    def delete(self, parcel_id):
        obj = self.get_by_id(parcel_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ------------------------------------------------------------------
    # CRUD nou pentru PDF uri cu schema dinamica
    # ------------------------------------------------------------------
    def save_document(self, original_filename, stored_filename, rows, column_metadata, extraction_mode="table"):
        document = UploadedDocument(
            original_filename=original_filename,
            stored_filename=stored_filename,
            row_count=len(rows),
            column_metadata=column_metadata,
            extraction_mode=extraction_mode,
        )
        self.db.add(document)
        self.db.flush()

        row_objects = []
        for index, row in enumerate(rows, start=1):
            row_objects.append(
                DocumentRow(
                    document_id=document.id,
                    row_number=index,
                    data=row,
                )
            )

        self.db.add_all(row_objects)
        self.db.commit()
        self.db.refresh(document)
        return document.id

    def list_documents(self, limit=10):
        return (
            self.db.query(UploadedDocument)
            .order_by(UploadedDocument.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_document(self, document_id):
        return (
            self.db.query(UploadedDocument)
            .filter(UploadedDocument.id == document_id)
            .first()
        )

    def get_document_rows(self, document_id):
        rows = (
            self.db.query(DocumentRow)
            .filter(DocumentRow.document_id == document_id)
            .order_by(DocumentRow.row_number.asc())
            .all()
        )
        return [row.data for row in rows]

    def delete_document(self, document_id):
        document = self.get_document(document_id)
        if not document:
            return False
        self.db.delete(document)
        self.db.commit()
        return True
