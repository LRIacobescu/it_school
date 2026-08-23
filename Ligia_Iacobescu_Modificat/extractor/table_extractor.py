import re
import pymupdf as fitz


class PDFTableExtractor:
    """
    Extrage tabele fara sa presupuna dinainte numele coloanelor

    Pentru PDF ul de taxe din proiect exista o normalizare suplimentara deoarece
    celula Owner contine laolalta ID, nume si adresa. Pentru alte PDF uri se
    pastreaza pur si simplu coloanele detectate de PyMuPDF
    """

    PARCEL_HEADERS = {
        "owner", "property description", "districts", "class",
        "acres", "land", "impts", "total"
    }

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract(self, max_pages=None):
        probe = fitz.open(self.pdf_path)
        try:
            page_count = len(probe)
            if max_pages is not None:
                page_count = min(page_count, max_pages)

            parcel_layout = self._detect_parcel_layout(probe)
        finally:
            probe.close()

        # Pentru PDF ul cunoscut structura tabelului este aceeasi pe toate
        # paginile. Detectam coloanele o singura data, apoi citim rapid celulele
        if parcel_layout:
            rows = self._extract_parcel_fast(page_count, parcel_layout)
            columns = list(rows[0].keys()) if rows else []
            if not rows:
                raise ValueError("Nu am gasit randuri in tabelul PDF.")
            return {
                "rows": rows,
                "columns": columns,
                "table_count": page_count,
                "page_count": page_count,
                "mode": "parcel_fast_table"
            }

        # Fallback generic: pentru orice alt PDF tabelar folosim find_tables()
        # pe fiecare pagina. Redeschidem documentul periodic pentru a evita
        # acumularea de memorie la documente mari
        rows = []
        table_count = 0
        chunk_size = 40

        for chunk_start in range(0, page_count, chunk_size):
            chunk_end = min(chunk_start + chunk_size, page_count)
            doc = fitz.open(self.pdf_path)
            try:
                for page_index in range(chunk_start, chunk_end):
                    page = doc.load_page(page_index)
                    found = page.find_tables()

                    for table in found.tables:
                        data = table.extract()
                        if not data or len(data) < 2:
                            continue

                        headers = self._normalise_headers(data[0])
                        if len(headers) < 2:
                            continue

                        table_count += 1
                        for raw_row in data[1:]:
                            if not raw_row or not any(self._clean_cell(value) for value in raw_row):
                                continue

                            cleaned_row = [self._clean_cell(value) for value in raw_row]
                            if self._looks_like_header_row(cleaned_row, headers):
                                continue

                            row = self._build_generic_row(headers, raw_row)
                            if row and any(value not in (None, "") for value in row.values()):
                                rows.append(row)
            finally:
                doc.close()

        if not rows:
            raise ValueError(
                "Nu am gasit un tabel cu date in PDF "
                "Aplicatia functioneaza cu PDF uri digitale/tabelare; pentru PDF uri scanate este necesar OCR"
            )

        columns = []
        for row in rows:
            for key in row.keys():
                if key not in columns:
                    columns.append(key)

        return {
            "rows": rows,
            "columns": columns,
            "table_count": table_count,
            "page_count": page_count,
            "mode": "pymupdf_tables"
        }

    def _detect_parcel_layout(self, doc):
        if len(doc) == 0:
            return None

        page = doc.load_page(0)
        found = page.find_tables()
        for table in found.tables:
            data = table.extract()
            if not data:
                continue
            headers = self._normalise_headers(data[0])
            if not self._is_parcel_table(headers):
                continue

            header_cells = table.rows[0].cells
            if len(header_cells) != len(headers):
                continue

            boundaries = [header_cells[0][0]]
            for cell in header_cells:
                boundaries.append(cell[2])

            return {
                "headers": headers,
                "boundaries": boundaries,
            }

        return None

    def _extract_parcel_fast(self, page_count, layout):
        import bisect

        rows = []
        boundaries = layout["boundaries"]
        headers = layout["headers"]
        parcel_pattern = re.compile(r"^\d{3}-\d{4}-\d{3}$")

        doc = fitz.open(self.pdf_path)
        try:
            for page_index in range(page_count):
                page = doc.load_page(page_index)
                words = page.get_text("words")
                parcel_words = [word for word in words if parcel_pattern.match(word[4])]
                parcel_words.sort(key=lambda word: word[1])

                if not parcel_words:
                    continue

                footer_y = page.rect.height - 20
                for word in words:
                    if word[4] == "Page" and word[1] > page.rect.height * 0.75:
                        footer_y = min(footer_y, word[1] - 4)

                row_tops = [word[1] - 0.7 for word in parcel_words]
                cell_words = [
                    [[] for _ in headers]
                    for _ in row_tops
                ]

                # O singura trecere prin cuvintele paginii. Este mult mai rapid
                # decat cate un get_textbox pentru fiecare celula
                for word in words:
                    x0, y0, x1, y1, text = word[:5]
                    center_x = (x0 + x1) / 2
                    center_y = (y0 + y1) / 2

                    if center_y < row_tops[0] or center_y >= footer_y:
                        continue

                    row_index = bisect.bisect_right(row_tops, center_y) - 1
                    if row_index < 0 or row_index >= len(row_tops):
                        continue

                    col_index = bisect.bisect_right(boundaries, center_x) - 1
                    if col_index < 0 or col_index >= len(headers):
                        continue

                    cell_words[row_index][col_index].append(word)

                for row_cells in cell_words:
                    raw_row = [self._words_to_text(words_in_cell) for words_in_cell in row_cells]
                    row = self._normalise_parcel_row(headers, raw_row)
                    if row.get("Parcel ID"):
                        rows.append(row)
        finally:
            doc.close()

        return rows

    def _words_to_text(self, words):
        if not words:
            return ""

        words = sorted(words, key=lambda word: (round(word[1], 1), word[0]))
        lines = []
        current_words = []
        current_y = None

        for word in words:
            y = word[1]
            if current_y is None or abs(y - current_y) <= 2.0:
                current_words.append(word[4])
                if current_y is None:
                    current_y = y
            else:
                lines.append(" ".join(current_words))
                current_words = [word[4]]
                current_y = y

        if current_words:
            lines.append(" ".join(current_words))

        return "\n".join(lines)

    def _normalise_headers(self, raw_headers):
        headers = []
        used = {}

        for index, value in enumerate(raw_headers):
            name = self._clean_cell(value)
            if not name:
                name = "Column " + str(index + 1)

            # Evitam doua chei JSON identice daca PDF ul are headere duplicate
            if name in used:
                used[name] += 1
                name = name + " " + str(used[name])
            else:
                used[name] = 1

            headers.append(name)

        return headers

    def _clean_cell(self, value):
        if value is None:
            return ""
        text = str(value).replace("\r", "\n")
        lines = []
        for line in text.split("\n"):
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                lines.append(line)
        return " | ".join(lines)

    def _cell_lines(self, value):
        if value is None:
            return []
        result = []
        for line in str(value).replace("\r", "\n").split("\n"):
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                result.append(line)
        return result

    def _is_parcel_table(self, headers):
        lowered = {header.lower() for header in headers}
        return self.PARCEL_HEADERS.issubset(lowered)

    def _looks_like_header_row(self, row, headers):
        if len(row) != len(headers):
            return False
        matches = 0
        for value, header in zip(row, headers):
            if value.strip().lower() == header.strip().lower():
                matches += 1
        return matches >= max(2, len(headers) // 2)

    def _build_generic_row(self, headers, raw_row):
        row = {}
        for index, header in enumerate(headers):
            value = raw_row[index] if index < len(raw_row) else None
            row[header] = self._clean_cell(value)
        return row

    def _first_value(self, value):
        lines = self._cell_lines(value)
        for line in lines:
            if line.lower() != "totals":
                return line
        return ""

    def _normalise_parcel_row(self, headers, raw_row):
        source = {}
        for index, header in enumerate(headers):
            source[header.lower()] = raw_row[index] if index < len(raw_row) else None

        owner_lines = self._cell_lines(source.get("owner"))
        parcel_id = ""
        owner = ""
        owner_address = ""
        owner_city = ""
        owner_state = ""
        owner_zip = ""

        if owner_lines:
            if re.match(r"^\d{3}-\d{4}-\d{3}$", owner_lines[0]):
                parcel_id = owner_lines[0]
                owner_lines = owner_lines[1:]

            city_index = None
            for index in range(len(owner_lines) - 1, -1, -1):
                match = re.match(r"^(.+?)\s+([A-Z]{2})\s+(\d{5,9}(?:-\d{4})?)$", owner_lines[index])
                if match:
                    city_index = index
                    owner_city = match.group(1).strip()
                    owner_state = match.group(2)
                    owner_zip = match.group(3)
                    break

            if city_index is not None:
                if city_index - 1 >= 0:
                    owner_address = owner_lines[city_index - 1]
                    name_lines = owner_lines[:city_index - 1]
                else:
                    name_lines = owner_lines[:city_index]
            else:
                name_lines = owner_lines

            owner = " / ".join(name_lines)

        property_lines = self._cell_lines(source.get("property description"))
        property_address = ""
        description_lines = []
        for line in property_lines:
            if re.match(r"^\d+\s+[A-Za-z]", line) and not property_address:
                property_address = line
                continue
            lower_line = line.lower()
            if "section:" in lower_line or "acres:" in lower_line:
                continue
            if re.match(r"^\d+\.\d+$", line):
                continue
            description_lines.append(line)
        property_description = " ".join(description_lines)

        district_lines = self._cell_lines(source.get("districts"))
        districts = []
        for line in district_lines:
            if re.match(r"^\d+$", line):
                continue
            districts.append(line)

        class_value = self._first_value(source.get("class"))
        acres = self._parse_number(self._first_value(source.get("acres")))
        land = self._first_money(source.get("land"))
        impts = self._first_money(source.get("impts"))
        total = self._first_money(source.get("total"))

        row = {
            "Parcel ID": parcel_id,
            "Owner": owner,
            "Owner Address": owner_address,
            "Owner City": owner_city,
            "Owner State": owner_state,
            "Owner ZIP": owner_zip,
            "Property Address": property_address,
            "Property Description": property_description,
            "District 1": districts[0] if len(districts) > 0 else "",
            "District 2": districts[1] if len(districts) > 1 else "",
            "District 3": districts[2] if len(districts) > 2 else "",
            "Class": class_value,
            "Acres": acres,
            "Land": land,
            "Impts": impts,
            "Total": total,
        }
        return row

    def _first_money(self, value):
        for line in self._cell_lines(value):
            if re.match(r"^[\$€£]?\s*-?[\d,]+(?:\.\d+)?$", line):
                return line
        return self._first_value(value)

    def _parse_number(self, value):
        if value in (None, ""):
            return None
        text = str(value).replace(",", "").strip()
        try:
            return float(text)
        except ValueError:
            return None
