import re


class PDFParser:
    def __init__(self, text):
        self.text = text or ""
        self.lines = [line.strip() for line in self.text.split("\n") if line.strip()]

    def clean_text(self):
        """Curata spatii multiple, linii goale si cateva simboluri decorative."""
        cleaned_lines = []
        for raw_line in self.text.splitlines():
            line = raw_line.replace("©", "").replace("®", "").replace("™", "")
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

    def extract_key_values(self):
        """Extrage linii simple de forma Cheie: Valoare."""
        result = {}
        for line in self.clean_text().splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key and value:
                result[key] = value
        return result

    def is_parcel_start(self, line):
        return bool(re.match(r"^\d{3}-\d{4}-\d{3}$", line))

    def is_footer(self, line):
        return bool(
            "Total properties listed" in line or
            re.search(r"Page \d+ of \d+", line)
        )

    def extract_all_parcels(self):
        """Parser legacy. Nu se mai opreste dupa primul footer de pagina."""
        parcels = []
        current = []

        for line in self.lines:
            if self.is_footer(line):
                # Footerul inchide parcela curenta, dar PDF ul poate continua
                # pe sute de pagini. In varianta veche era `break` si se oprea
                # complet dupa prima pagina.
                if current and self.is_parcel_start(current[0]):
                    parcel = self.parse_parcel(current)
                    if parcel:
                        parcels.append(parcel)
                current = []
                continue

            if not current and not self.is_parcel_start(line):
                continue

            if self.is_parcel_start(line):
                if current:
                    parcel = self.parse_parcel(current)
                    if parcel:
                        parcels.append(parcel)
                current = [line]
                continue

            current.append(line)

        if current and self.is_parcel_start(current[0]):
            parcel = self.parse_parcel(current)
            if parcel:
                parcels.append(parcel)

        return parcels

    def parse_parcel(self, blocks):
        parcel = {
            "parcel_id": blocks[0],
            "owner_name": None,
            "owner_street": None,
            "city": None,
            "state": None,
            "zip_code": None,
            "prop_address_1": None,
            "prop_address_2": None,
            "section": "",
            "prop_acres": None,
            "district_1": None,
            "district_2": None,
            "district_3": None,
            "class_value": None,
            "acres": None,
            "land": None,
            "impts": None,
            "total": None
        }

        # Format artificial folosit de testele initiale.
        if any("District 1:" in line for line in blocks):
            parcel["owner_name"] = blocks[1] if len(blocks) > 1 else None
            parcel["owner_street"] = blocks[2] if len(blocks) > 2 else None

            if len(blocks) > 3:
                city_line = blocks[3]
                match = re.match(r"(.+?)\s+([A-Z]{2})(?:\s+(\d{5,9}))?$", city_line)
                if match:
                    parcel["city"] = match.group(1).strip()
                    parcel["state"] = match.group(2)
                    parcel["zip_code"] = match.group(3)

            # In formatul de test adresa proprietatii apare dupa city/state.
            if len(blocks) > 4:
                parcel["prop_address_1"] = blocks[4]

            for line in blocks:
                if line.startswith("SECTION"):
                    parcel["section"] = line.replace("SECTION", "").strip()

                match = re.search(r"^Acres:\s*([\d.]+)", line)
                if match:
                    parcel["prop_acres"] = float(match.group(1))

                if line.startswith("District 1"):
                    parcel["district_1"] = line.split(":", 1)[1].strip()
                elif line.startswith("District 2"):
                    parcel["district_2"] = line.split(":", 1)[1].strip()
                elif line.startswith("District 3"):
                    parcel["district_3"] = line.split(":", 1)[1].strip()
                elif line.startswith("Class:"):
                    parcel["class_value"] = line.split(":", 1)[1].strip()
                elif line.startswith("Land:"):
                    parcel["land"] = line.split(":", 1)[1].strip()
                elif line.startswith("Impts:"):
                    parcel["impts"] = line.split(":", 1)[1].strip()
                elif line.startswith("Total:"):
                    parcel["total"] = line.split(":", 1)[1].strip()

                match = re.search(r"Acres Total:\s*([\d.]+)", line)
                if match:
                    parcel["acres"] = float(match.group(1))

            return parcel

        # Parserul legacy ramane disponibil pentru scripturile vechi, dar
        # aplicatia web foloseste extractia tabelara, mult mai corecta.
        if len(blocks) > 1:
            parcel["prop_address_1"] = blocks[1]

        district_lines = []
        for line in blocks[2:]:
            if any(key in line for key in ["Dist", "MATC", "Metro", "TID"]):
                district_lines.append(line)
        if district_lines:
            parcel["district_1"] = district_lines[0] if len(district_lines) > 0 else None
            parcel["district_2"] = district_lines[1] if len(district_lines) > 1 else None
            parcel["district_3"] = district_lines[2] if len(district_lines) > 2 else None

        city_idx = None
        for index, line in enumerate(blocks):
            if re.search(r"[A-Z]{2}\s+\d{5,9}$", line):
                city_idx = index
                break

        if city_idx is not None:
            match = re.match(r"(.+?)\s+([A-Z]{2})\s+(\d{5,9})$", blocks[city_idx])
            if match:
                parcel["city"] = match.group(1).strip()
                parcel["state"] = match.group(2)
                parcel["zip_code"] = match.group(3)
            if city_idx - 2 >= 0:
                parcel["owner_name"] = blocks[city_idx - 2].strip()
            if city_idx - 1 >= 0:
                parcel["owner_street"] = blocks[city_idx - 1].strip()

        numeric_acres = []
        for line in blocks:
            if re.match(r"^\d+\.\d+$", line.strip()):
                numeric_acres.append(float(line.strip()))
        if numeric_acres:
            parcel["prop_acres"] = numeric_acres[0]
            parcel["acres"] = numeric_acres[-1]

        dollar_values = [line for line in blocks if re.match(r"^\$[\d,]+(?:\.\d+)?$", line)]
        if dollar_values:
            parcel["land"] = dollar_values[0]
            if len(dollar_values) > 1:
                parcel["impts"] = dollar_values[1]
            if len(dollar_values) > 2:
                # Prima triada Land / Impts / Total este mai sigura decat
                # ultimul element, care in PDF ul original era adesea Land.
                parcel["total"] = dollar_values[2]
            else:
                parcel["total"] = dollar_values[-1]

        for line in blocks:
            if re.match(r"^[A-Z]\d$", line.strip()):
                parcel["class_value"] = line.strip()
                break

        return parcel if parcel["prop_acres"] is not None else None
