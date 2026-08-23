import json
from extractor.reader import PDFReader
from extractor.parser import PDFParser
from config.settings import settings

# Color codes for terminal
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def print_section(title):
    print(f"\n{CYAN}{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}{RESET}\n")


def highlight_missing(parcel):
    missing = []
    for key, value in parcel.items():
        if value is None or value == "":
            missing.append(key)
    return missing


def debug_parcel(parcel, index):
    print_section(f"Parcel #{index + 1} — {parcel.get('parcel_id', 'UNKNOWN')}")

    for key, value in parcel.items():
        if value is None or value == "":
            print(f"{RED}{key}: {value}{RESET}")
        else:
            print(f"{GREEN}{key}: {value}{RESET}")

    missing = highlight_missing(parcel)
    if missing:
        print(f"\n{YELLOW}⚠ Missing fields: {', '.join(missing)}{RESET}")
    else:
        print(f"{GREEN}✔ All fields extracted successfully{RESET}")


def debug_blocks(raw_text):
    print_section("RAW BLOCKS DETECTED")

    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    blocks = []
    current = []

    import re
    for line in lines:
        if re.match(r"\d{3}-\d{4}-\d{3}", line):
            if current:
                blocks.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        blocks.append("\n".join(current))

    for i, block in enumerate(blocks):
        print_section(f"BLOCK #{i + 1}")
        print(block)


def run_debug():
    print_section("DEBUGGING PARSER")

    # 1. Read PDF
    reader = PDFReader(settings.PDF_PATH)
    extracted = reader.auto_extract()
    raw_text = extracted["text"]

    print_section("PDF TYPE")
    print(extracted["type"])

    print_section("RAW TEXT LENGTH")
    print(len(raw_text))

    # 2. Show raw blocks
    debug_blocks(raw_text)

    # 3. Parse parcels
    parser = PDFParser(raw_text)
    parcels = parser.extract_all_parcels()

    print_section("TOTAL PARCELS DETECTED")
    print(len(parcels))

    # 4. Debug each parcel
    for i, parcel in enumerate(parcels):
        debug_parcel(parcel, i)

    print_section("JSON OUTPUT (first parcel)")
    print(json.dumps(parcels[0], indent=4))


if __name__ == "__main__":
    run_debug()
