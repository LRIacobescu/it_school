import sys
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from extractor.reader import PDFReader
from config.settings import settings

reader = PDFReader(settings.PDF_PATH)
text = reader.extract_text_blocks()

lines = text.split("\n")

parcel = []
started = False

for line in lines:
    if re.match(r"^\d{3}-\d{4}-\d{3}$", line):
        if started:
            break
        started = True

    if started:
        parcel.append(line)

print("\n================ FIRST PARCEL ================\n")
print("\n".join(parcel))
print("\n==============================================\n")
