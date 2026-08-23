import pymupdf as fitz


class PDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_blocks(self):
        """Extrage textul brut in ordinea vizuala a paginii"""
        doc = fitz.open(self.pdf_path)
        full_text = []

        try:
            for page in doc:
                blocks = page.get_text("blocks")
                blocks = sorted(blocks, key=lambda block: (block[1], block[0]))
                for block in blocks:
                    text = block[4].strip()
                    if text:
                        full_text.append(text)
        finally:
            doc.close()

        return "\n".join(full_text)

    def extract_text(self):
        """Alias pastrat pentru testele/scripturile vechi."""
        return self.extract_text_blocks()

    def extract_tables(self, max_pages=None):
        """Extrage tabelele detectate de PyMuPDF ca liste de randuri."""
        doc = fitz.open(self.pdf_path)
        tables = []

        try:
            page_count = len(doc)
            if max_pages is not None:
                page_count = min(page_count, max_pages)

            for page_index in range(page_count):
                page = doc[page_index]
                found = page.find_tables()
                for table in found.tables:
                    data = table.extract()
                    if data:
                        tables.append(data)
        finally:
            doc.close()

        return tables

    def extract(self):
        return {
            "type": "digital",
            "text": self.extract_text_blocks(),
            "tables": []
        }

    def auto_extract(self):
        # Nu rulam find_tables aici pentru tot PDF ul deoarece ar dubla munca
        # Aplicatia web foloseste PDFTableExtractor pentru tabele
        return self.extract()
