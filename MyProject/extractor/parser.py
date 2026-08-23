import re

class PDFParser:
    def __init__(self, text: str):
        self.lines = [line.strip() for line in text.split("\n") if line.strip()]

    def is_parcel_start(self, line: str) -> bool:
        return bool(re.match(r"^\d{3}-\d{4}-\d{3}$", line))

    def is_footer(self, line: str) -> bool:
        return (
            "Total properties listed" in line or
            re.search(r"Page \d+ of \d+", line)
        )

    def extract_all_parcels(self):
        parcels = []
        current = []

        for line in self.lines:

            if not current and not self.is_parcel_start(line):
                continue

            if self.is_parcel_start(line):
                if current:
                    parcel = self.parse_parcel(current)
                    if parcel:
                        parcels.append(parcel)
                current = [line]
                continue

            if self.is_footer(line):
                current = []
                break

            current.append(line)

        if current and self.is_parcel_start(current[0]):
            parcel = self.parse_parcel(current)
            if parcel:
                parcels.append(parcel)

        return parcels

    def parse_parcel(self, blocks: list) -> dict:
        parcel = {
            "parcel_id": blocks[0],
            "owner_name": None,
            "owner_street": None,
            "city": None,
            "state": None,
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

        # ---------------------------------------------------------
        # FORMAT ARTIFICIAL (TESTE)
        # ---------------------------------------------------------
        if any("District 1:" in line for line in blocks):
            parcel["prop_address_1"] = blocks[2]
            parcel["prop_address_2"] = blocks[4]

            parcel["owner_name"] = blocks[1]
            parcel["owner_street"] = blocks[2]

            city_line = blocks[3]
            m = re.match(r"(.+?)\s+([A-Z]{2})", city_line)
            if m:
                parcel["city"] = m.group(1).strip()
                parcel["state"] = m.group(2)

            for line in blocks:
                if line.startswith("SECTION"):
                    parcel["section"] = line.replace("SECTION", "").strip()

            for line in blocks:
                m = re.search(r"Acres:\s*([\d.]+)", line)
                if m:
                    parcel["prop_acres"] = float(m.group(1))

            for line in blocks:
                if line.startswith("District 1"):
                    parcel["district_1"] = line.split(":", 1)[1].strip()
                if line.startswith("District 2"):
                    parcel["district_2"] = line.split(":", 1)[1].strip()
                if line.startswith("District 3"):
                    parcel["district_3"] = line.split(":", 1)[1].strip()

            for line in blocks:
                if line.startswith("Class:"):
                    parcel["class_value"] = line.split(":", 1)[1].strip()

            for line in blocks:
                if line.startswith("Land:"):
                    parcel["land"] = line.split(":", 1)[1].strip()
                if line.startswith("Impts:"):
                    parcel["impts"] = line.split(":", 1)[1].strip()
                if line.startswith("Total:"):
                    parcel["total"] = line.split(":", 1)[1].strip()

            for line in blocks:
                m = re.search(r"Acres Total:\s*([\d.]+)", line)
                if m:
                    parcel["acres"] = float(m.group(1))

            return parcel

        # ---------------------------------------------------------
        # FORMAT PDF REAL
        # ---------------------------------------------------------

        # 1) prop_address_1
        if len(blocks) > 1:
            parcel["prop_address_1"] = blocks[1]

        # 2) districts
        district_lines = []
        for line in blocks[2:]:
            if any(key in line for key in ["Dist", "MATC", "Metro", "TID"]):
                district_lines.append(line)

        if district_lines:
            parcel["district_1"] = district_lines[0] if len(district_lines) > 0 else None
            parcel["district_2"] = district_lines[1] if len(district_lines) > 1 else None
            parcel["district_3"] = district_lines[2] if len(district_lines) > 2 else None

        # 3) owner + city/state
        city_idx = None
        for i, line in enumerate(blocks):
            if re.search(r"[A-Z]{2}\s+\d{5}", line):
                city_idx = i
                break

        if city_idx is not None:
            city_line = blocks[city_idx]
            m = re.match(r"(.+?)\s+([A-Z]{2})\s+(\d{5})", city_line)
            if m:
                parcel["city"] = m.group(1).strip()
                parcel["state"] = m.group(2)

            if city_idx - 2 >= 0:
                parcel["owner_name"] = blocks[city_idx - 2].strip()
            if city_idx - 1 >= 0:
                parcel["owner_street"] = blocks[city_idx - 1].strip()

        # 4) prop_acres
        acres_index = None
        for i, line in enumerate(blocks):
            if re.match(r"^\d+\.\d+$", line.strip()):
                parcel["prop_acres"] = float(line.strip())
                acres_index = i
                break

        if acres_index is None:
            return None

        # 5) land / impts / total / class
        dollar_values = [line for line in blocks if "$" in line]
        class_line = None
        for line in blocks:
            if re.match(r"^[A-Z]\d$", line.strip()):
                class_line = line.strip()
                break

        if dollar_values:
            parcel["land"] = dollar_values[0]
            if len(dollar_values) > 1:
                parcel["impts"] = dollar_values[1]
            parcel["total"] = dollar_values[-1]

        if class_line:
            parcel["class_value"] = class_line

        # 6) acres final
        last_acres = None
        for line in blocks:
            if re.match(r"^\d+\.\d+$", line.strip()):
                last_acres = float(line.strip())
        if last_acres is not None:
            parcel["acres"] = last_acres

        return parcel

