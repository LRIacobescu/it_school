import io
import os
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle


_REGISTERED_FONT_NAMES = None


def _register_fonts():
    """Incearca sa foloseasca un font Unicode existent pe sistem, fara sa il includa in proiect."""
    global _REGISTERED_FONT_NAMES
    if _REGISTERED_FONT_NAMES:
        return _REGISTERED_FONT_NAMES

    candidates = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ),
        (
            "/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial Bold.ttf",
        ),
        (
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ),
    ]

    for regular_path, bold_path in candidates:
        if os.path.exists(regular_path) and os.path.exists(bold_path):
            try:
                pdfmetrics.registerFont(TTFont("PDFExportFont", regular_path))
                pdfmetrics.registerFont(TTFont("PDFExportFontBold", bold_path))
                _REGISTERED_FONT_NAMES = ("PDFExportFont", "PDFExportFontBold")
                return _REGISTERED_FONT_NAMES
            except Exception:
                pass

    # Fallback ul functioneaza fara fisiere de font suplimentare.
    _REGISTERED_FONT_NAMES = ("Helvetica", "Helvetica-Bold")
    return _REGISTERED_FONT_NAMES


def _clean_text(value):
    if value is None:
        return ""

    text = str(value).replace("\x00", "").strip()

    # Evitam caractere de control care pot strica documentul PDF.
    text = "".join(character for character in text if character >= " " or character in "\n\t")
    return escape(text).replace("\n", "<br/>")


def _filter_summary(filters, metadata, search_text):
    metadata_map = {item["name"]: item for item in metadata}
    parts = []

    search_text = (search_text or "").strip()
    if search_text:
        parts.append("Cautare globala: " + search_text)

    for column, spec in (filters or {}).items():
        column_type = metadata_map.get(column, {}).get("type")

        if column_type == "text":
            values = spec.get("values") or []
            if values:
                parts.append(column + ": " + ", ".join(str(value) for value in values))
        else:
            minimum = spec.get("min")
            maximum = spec.get("max")
            if minimum not in (None, "") or maximum not in (None, ""):
                left = str(minimum) if minimum not in (None, "") else "fara minim"
                right = str(maximum) if maximum not in (None, "") else "fara maxim"
                parts.append(column + ": " + left + " - " + right)

    if not parts:
        return "Fara filtre - sunt exportate toate randurile documentului."

    return " | ".join(parts)


def _column_widths(columns, rows, available_width):
    """Calculeaza latimi dinamice, dar pastreaza tabelul in interiorul paginii."""
    if not columns:
        return []

    weights = []
    sample_rows = rows[:120]

    for column in columns:
        longest = len(str(column))
        for row in sample_rows:
            longest = max(longest, len(str(row.get(column, "") or "")))

        # Coloanele foarte lungi primesc mai mult spatiu, fara sa acapareze pagina.
        weights.append(max(8, min(longest, 30)))

    total_weight = sum(weights) or 1
    minimum_width = 22 * mm
    widths = [available_width * weight / total_weight for weight in weights]

    # Daca sunt putine coloane, evitam coloane exagerat de inguste.
    if len(columns) <= 8:
        widths = [max(minimum_width, width) for width in widths]
        scale = available_width / sum(widths)
        widths = [width * scale for width in widths]

    return widths


def build_filtered_pdf(document_name, rows, metadata, filters=None, search_text=""):
    """Genereaza in memorie un PDF cu toate randurile primite."""
    regular_font, bold_font = _register_fonts()
    columns = [item["name"] for item in metadata]

    # Pentru multe coloane folosim A3 landscape, altfel A4 landscape.
    page_size = landscape(A3) if len(columns) > 8 else landscape(A4)
    left_margin = 12 * mm
    right_margin = 12 * mm
    top_margin = 15 * mm
    bottom_margin = 15 * mm

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        title="Date filtrate - " + str(document_name),
        author="PDF Data Explorer",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ExportTitle",
        parent=styles["Heading1"],
        fontName=bold_font,
        fontSize=16,
        leading=19,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=4,
    )
    info_style = ParagraphStyle(
        "ExportInfo",
        parent=styles["BodyText"],
        fontName=regular_font,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#5D6678"),
        alignment=TA_LEFT,
    )
    header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["BodyText"],
        fontName=bold_font,
        fontSize=6.2 if len(columns) > 8 else 7.2,
        leading=7.2 if len(columns) > 8 else 8.3,
        textColor=colors.white,
    )
    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["BodyText"],
        fontName=regular_font,
        fontSize=5.7 if len(columns) > 8 else 6.7,
        leading=7.0 if len(columns) > 8 else 8.0,
        textColor=colors.HexColor("#2F3747"),
    )

    story = [
        Paragraph("Date filtrate", title_style),
        Paragraph("Document sursa: " + _clean_text(document_name), info_style),
        Paragraph("Randuri exportate: " + str(len(rows)), info_style),
        Paragraph("Generat: " + datetime.now().strftime("%d.%m.%Y %H:%M"), info_style),
        Spacer(1, 3 * mm),
        Paragraph("Filtre aplicate: " + _clean_text(_filter_summary(filters, metadata, search_text)), info_style),
        Spacer(1, 5 * mm),
    ]

    if not columns:
        story.append(Paragraph("Documentul nu contine coloane care pot fi exportate.", info_style))
    elif not rows:
        story.append(Paragraph("Niciun rand nu corespunde filtrelor selectate.", info_style))
    else:
        available_width = page_size[0] - left_margin - right_margin
        widths = _column_widths(columns, rows, available_width)

        table_data = [
            [Paragraph(_clean_text(column), header_style) for column in columns]
        ]

        for row in rows:
            table_data.append([
                Paragraph(_clean_text(row.get(column, "")), cell_style)
                for column in columns
            ])

        table = LongTable(
            table_data,
            colWidths=widths,
            repeatRows=1,
            splitByRow=1,
            hAlign="LEFT",
        )
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2457FF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDE3EE")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFD")]),
        ]))
        story.append(table)

    def draw_footer(canvas, current_doc):
        canvas.saveState()
        canvas.setFont(regular_font, 7)
        canvas.setFillColor(colors.HexColor("#7B8494"))
        canvas.drawString(left_margin, 7 * mm, "PDF Data Explorer")
        canvas.drawRightString(page_size[0] - right_margin, 7 * mm, "Pagina " + str(current_doc.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return buffer.getvalue()
