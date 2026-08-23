from extractor.table_extractor import PDFTableExtractor


class PDFExtractor:
    """
    Wrapper compatibil cu proiectul initial.

    Pentru PDF ul de parcele transforma randurile tabelare corecte inapoi in
    structura veche folosita de validator si PDFData. Pentru alte PDF uri,
    aplicatia web foloseste direct PDFTableExtractor si schema dinamica
    """

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract(self, max_pages=None):
        result = PDFTableExtractor(self.pdf_path).extract(max_pages=max_pages)
        rows = result["rows"]

        if not rows or "Parcel ID" not in rows[0]:
            return rows

        parcels = []
        for row in rows:
            parcels.append({
                "parcel_id": row.get("Parcel ID"),
                "owner_name": row.get("Owner"),
                "owner_street": row.get("Owner Address"),
                "city": row.get("Owner City"),
                "state": row.get("Owner State"),
                "zip_code": row.get("Owner ZIP"),
                "prop_address_1": row.get("Property Address"),
                # Modelul vechi nu avea camp separat pentru description.
                "prop_address_2": row.get("Property Description"),
                "section": "",
                "prop_acres": row.get("Acres"),
                "district_1": row.get("District 1"),
                "district_2": row.get("District 2"),
                "district_3": row.get("District 3"),
                "class_value": row.get("Class"),
                "acres": row.get("Acres"),
                "land": row.get("Land"),
                "impts": row.get("Impts"),
                "total": row.get("Total"),
            })

        return parcels
