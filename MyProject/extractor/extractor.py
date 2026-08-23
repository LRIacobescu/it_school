import re
from extractor.reader import PDFReader
from extractor.parser import PDFParser


class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.reader = PDFReader(pdf_path)

        # HEADERE PDF reale
        self.HEADER_PATTERNS = [
            "Completed Real Estate Assessment Roll",
            "Manufacturing values suppressed",
            "Sorted by tax key number",
            "Property Description",
            "Districts",
            "Class Acres Land Impts Total",
            "Assessment Roll",
            "Real Estate",
            "Tax Key",
        ]

    # ----------------------------------------------------------------------
    # 1. CURĂȚARE TEXT (MINIMALĂ)
    # ----------------------------------------------------------------------
    def clean_lines(self, text: str) -> list:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        cleaned = []

        for line in lines:

            # HEADER PDF
            if any(pattern in line for pattern in self.HEADER_PATTERNS):
                continue

            # FOOTER
            if re.search(r"Page \d+ of \d+", line):
                continue
            if "City of Saint Francis" in line:
                continue

            # REZUMAT
            if "Total properties listed" in line:
                continue
            if "Total acres and values by class" in line:
                continue

            cleaned.append(line)

        return cleaned

    # ----------------------------------------------------------------------
    # 2. RECONSTRUIRE PARCEL ID (FĂRĂ ID-URI FALSE)
    # ----------------------------------------------------------------------
    def reconstruct_parcel_ids(self, lines: list) -> list:
        reconstructed = []
        last_id = None

        for line in lines:

            # detectăm parcel_id real
            if re.match(r"^\d{3}-\d{4}-\d{3}$", line):
                last_id = line
                reconstructed.append(line)
                continue

            # păstrăm doar liniile care apar DUPĂ un parcel_id real
            if last_id:
                reconstructed.append(line)

        return reconstructed

    # ----------------------------------------------------------------------
    # 3. GRUPARE ÎN PARCELE
    # ----------------------------------------------------------------------
    def group_into_parcels(self, lines: list) -> list:
        parcels = []
        current = []

        for line in lines:

            if re.match(r"^\d{3}-\d{4}-\d{3}$", line):
                if current:
                    parcels.append(current)
                current = [line]
            else:
                current.append(line)

        if current:
            parcels.append(current)

        return parcels

    # ----------------------------------------------------------------------
    # 4. PIPELINE COMPLET
    # ----------------------------------------------------------------------
    def extract(self):
        raw_text = self.reader.extract_text_blocks()

        cleaned = self.clean_lines(raw_text)
        reconstructed = self.reconstruct_parcel_ids(cleaned)
        grouped = self.group_into_parcels(reconstructed)

        parser = PDFParser(raw_text)

        final_parcels = []
        for parcel_lines in grouped:

            # --------------------------------------------------------------
            # FILTRARE MINIMALĂ (lăsăm parserul universal să decidă)
            # --------------------------------------------------------------

            # trebuie să înceapă cu parcel_id real
            if not re.match(r"^\d{3}-\d{4}-\d{3}$", parcel_lines[0]):
                continue

            # trebuie să conțină cel puțin o adresă
            if not any(re.match(r"^\d{3,5}\s+[A-Za-z]", line) for line in parcel_lines):
                continue

            parcel = parser.parse_parcel(parcel_lines)
            if parcel:
                final_parcels.append(parcel)

        return final_parcels
