import fitz  # PyMuPDF

class PDFReader:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text_blocks(self) -> str:
        """
        Extrage textul în ordinea vizuală a PDF-ului.
        NU filtrează nimic.
        Filtrarea se face în extractor.
        """
        doc = fitz.open(self.pdf_path)
        full_text = []

        for page in doc:
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # sortare vizuală

            for block in blocks:
                text = block[4].strip()
                if text:
                    full_text.append(text)

        doc.close()
        return "\n".join(full_text)

    def extract(self) -> dict:
        return {
            "type": "digital",
            "text": self.extract_text_blocks(),
            "tables": None
        }

    def auto_extract(self) -> dict:
        return {
            "type": "digital",
            "text": self.extract_text_blocks(),
            "tables": None
        }
